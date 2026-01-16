import platform
import requests
import dacite
from requests import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from typing import List

import util.utils as utils
from core.dates import DateHandler
from common.typing import (
    BusArrival,
    GeoFoxResponse,
    GeoFoxDeparture,
    GeoFoxDepartureLine,
    GeoFoxDepartureLineType,
    GeoFoxDepartureStation,
    GeoFoxTime
)
from common.logger import log_event


class HVV:
    def __init__(
        self,
        dh: DateHandler
    ) -> None:
        self.HVV_URL = "https://www.hvv.de/de/fahrplaene/abruf-fahrplaninfos/abfahrten-auf-ihrem-monitor/abfahrten-anzeige?show=028d4278b61c4485a4e6bd8c9a1c115e"
        self.GEOFOX_URL = "https://www.hvv.de/geofox/departureList"
        self.busses: List[BusArrival] = []
        
        self.dh = dh

    @property
    def geofox_header(self) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
    
    @property
    def geofox_payload(self) -> dict:
        date = self.dh.date.strftime("%d.%m.%Y")
        time = self.dh.date.strftime("%M:%S")
        return {
            "version": 47,
            "stations": [
                {"name": "Alfred-Mahlau-Weg", "id": "Master:70050", "city": "Hamburg", "type": "STATION"}
            ],
            "filter": [
                {"serviceID": "HHA-B:26_HHA-B", "stationIDs": ["Master:70053"]},
                {"serviceID": "HHA-B:26_HHA-B", "stationIDs": ["Master:70060"]},
                {"serviceID": "HHA-B:218_HHA-B", "stationIDs": ["Master:70053"]},
                {"serviceID": "HHA-B:218_HHA-B", "stationIDs": ["Master:70054"]},
            ],
            "time": {"date": date, "time": time},
            "maxList": 10,
            "allStationsInChangingNode": True,
            "maxTimeOffset": 200,
            "useRealtime": True,
        }

    @property
    def next_busses(self) -> List[BusArrival]:
        already_added_bus = set()
        busses: List[BusArrival] = []
        max_len = 3

        for bus in self.busses:
            if bus.destination in already_added_bus:
                continue
            
            already_added_bus.add(bus.destination)
            busses.append(bus)
            
            if len(busses) >= max_len:
                break
        return busses

    def _to_datetime(
        self,
        time: str
    ) -> datetime:
        now = utils.tz_date()
        hour, minute = time.split(":")
        return datetime(now.year, now.month, now.day, int(hour), int(minute), now.second)

    @log_event("Getting arrivals list...")
    def _scrape_arrivals(
        self,
        driver: webdriver.Chrome
    ) -> List[BusArrival]:
        rows = driver.find_elements(By.CSS_SELECTOR, "tr.js-tr-monitor-departure")
        busses: List[BusArrival] = []
        
        for row in rows:
            try:
                line_elem = row.find_element(By.CSS_SELECTOR, ".o-transport-icon__number")
                line = int(line_elem.text)
            except:
                line = -1
            
            destination = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            destination = destination.replace(" ", "")
            
            arrival_info = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            arrival_info = arrival_info.split("+")

            time = self._to_datetime(arrival_info[0])
            delay_minutes = int(arrival_info[1]) if len(arrival_info) > 1 else 0
            delay = timedelta(minutes=delay_minutes)

            busses.append(
                BusArrival(
                    line=line,
                    destination=destination,
                    time=time,
                    delay=delay,
                )
            )
        return busses

    @log_event("Loading Chromium Drivers...")
    def _get_chrome_driver(self) -> webdriver.Chrome:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        machine = platform.uname()
        
        if machine.system == "Linux" and machine.machine == "armv7l":        # my Raspberry Pi 2 :)
            options.binary_location = "/usr/bin/chromium"
            service = Service("/usr/bin/chromedriver")
            return webdriver.Chrome(service=service, options=options)
        else:
            return webdriver.Chrome(options=options)
    
    def _convert_response(
        self,
        data: dict
    ) -> GeoFoxResponse:
        returnCode = data["returnCode"]
        time = dacite.from_dict(data_class=GeoFoxTime, data=data["time"])
        
        for idx, _ in enumerate(data["departures"]):
            if "delay" not in data["departures"][idx].keys():
                data["departures"][idx]["delay"] = 0
            
            line_type = dacite.from_dict(data_class=GeoFoxDepartureLineType, data=data["departures"][idx]["line"]["type"])
            line = dacite.from_dict(data_class=GeoFoxDepartureLine, data=data["departures"][idx]["line"])
            station = dacite.from_dict(data_class=GeoFoxDepartureStation, data=data["departures"][idx]["station"])
            departure = dacite.from_dict(data_class=GeoFoxDeparture, data=data["departures"][idx])
            
            data["departures"][idx]["line"]["type"] = line_type
            data["departures"][idx]["line"] = line
            data["departures"][idx]["station"] = station
            data["departures"][idx] = departure
        return GeoFoxResponse(
            returnCode=returnCode,
            time=time,
            departures=data["departures"]
        )
    
    def _parse_geofox_data(
        self,
        rsp: GeoFoxResponse
    ) -> List[BusArrival]:
        busses = []
        section: GeoFoxDeparture
        
        for section in rsp.departures:
            if section.timeOffset < 0:
                time = self.dh.date - timedelta(minutes=abs(section.timeOffset))
            else:
                time = self.dh.date + timedelta(minutes=section.timeOffset)
            
            busses.append(
                BusArrival(
                    line=int(section.line.name), # "218"
                    destination=section.line.direction,
                    time=time,
                    delay=timedelta(seconds=section.delay)
                )
            )
        return busses
    
    @log_event("Sending request to HVV GeoFox")
    def get_geofox_response(self) -> GeoFoxResponse:
        try:
            rsp = requests.post(url=self.GEOFOX_URL, headers=self.geofox_header, json=self.geofox_payload, timeout=20).json()
            return self._convert_response(data=rsp)
        except exceptions.ReadTimeout as rte:
            log_event("Connection timeout")
        except exceptions.ConnectionError as ce:
            log_event("Site does not exist. Connection error")
        except Exception as e:
            print(e)
    
    @log_event("Getting bus arrivals...")
    def set_bus_arrivals(self) -> None:
        rsp = self.get_geofox_response()
        if rsp:
            self.busses = self._parse_geofox_data(rsp)
        else:
            driver = self._get_chrome_driver()
            try:
                driver.get(self.HVV_URL)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "tr.js-tr-monitor-departure")
                    )
                )
                self.busses = self._scrape_arrivals(driver)
            finally:
                driver.quit()