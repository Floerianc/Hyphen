import platform
import dacite
import random
from os import environ
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
from core.proxy import SessionWrapper
from common.typing import (
    BusArrival,
    GeoFoxResponse,
    GeoFoxDeparture,
    GeoFoxDepartureLine,
    GeoFoxDepartureLineType,
    GeoFoxDepartureStation,
    GeoFoxTime
)
from common.logger import (
    log_event,
    log_decorator
)


class HVV:
    def __init__(
        self,
        dh: DateHandler
    ) -> None:
        self.HVV_URL = environ.get("HVV_URL", "")
        self.GEOFOX_URL = environ.get("GEOFOX_URL", "")
        self.sleep_time = (22, 6)
        self.sleeping = False
        self.busses: List[BusArrival] = []
        
        self.dh = dh
        self.session = SessionWrapper(timeout=20)

    @property
    def geofox_header(self) -> dict:
        """Header for the GeoFox API

        Returns:
            dict: HTTP Header
        """
        
        UAs = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.111 Safari/537.36 Brave/1.75.175",
            "Mozilla/5.0 (Windows NT 11.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.84 Safari/537.36 Brave/1.75.175",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3563.62 Safari/537.36"
        ]
        
        return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "User-Agent": random.choice(UAs),
        }
    
    @property
    def geofox_payload(self) -> dict:
        """Payload for the GeoFox API call

        Here I use a random station and line but you can
        change this to use your nearest station.

        Returns:
            dict: Payload
        """
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
            "maxList": 15,
            "allStationsInChangingNode": True,
            "maxTimeOffset": 200,
            "useRealtime": True,
        }

    @property
    def next_busses(self) -> List[BusArrival]:
        """Returns the next few busses that arrive at your
        station. You can amount change the max stations
        in the function

        Note: This is a set which only adds new lines.
        So if you have a bus line 100 and the next bus
        is another bus line 100 it won't be added on the
        list. However, bus line 101 would be added if it's
        not already in the set.

        Returns:
            List[BusArrival]: Next busses
        """
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
        """Converts Hour:Minute to datetime

        Args:
            time (str): Time in Hour:Minute format

        Returns:
            datetime: datetime object
        """
        now = utils.tz_date()
        hour, minute = time.split(":")
        try:
            return datetime(now.year, now.month, now.day, int(hour), int(minute), now.second)
        except:
            log_event(
                f"Couldn't parse hour and minute from time {time}\n"
                "Note: time must be \"Hour:Minute\" format.",
                "ERROR"
            )
            return datetime(0, 0, 0, 0, 0, 0, 0)

    @log_decorator("Getting arrivals list...")
    def _scrape_arrivals(
        self,
        driver: webdriver.Chrome
    ) -> List[BusArrival]:
        """Scrapes next busses that arrive

        It uses the HVV_URL variable to load a chromium
        webdriver and scrape the next bus lines and the
        time they arrive at your station.

        Args:
            driver (webdriver.Chrome): Chromium Webdriver

        Returns:
            List[BusArrival]: Next busses
        """
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
            delay_minutes = int(arrival_info[1]) if len(arrival_info) > 0 else 0
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

    @log_decorator("Loading Chromium Drivers...")
    def _get_chrome_driver(self) -> webdriver.Chrome:
        """Returns a chromium webdriver

        Returns:
            webdriver.Chrome: Chromium webdriver
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        machine = platform.uname()
        
        try:
            if machine.system == "Linux" and machine.machine == "armv7l":        # my Raspberry Pi 2 :)
                options.binary_location = "/usr/bin/chromium"
                service = Service("/usr/bin/chromedriver")
                return webdriver.Chrome(service=service, options=options)
            else:
                return webdriver.Chrome(options=options)
        except Exception as e:
            msg = (f"Can't find Chromium webdriver for system {machine.system}"
            f"and machine {machine.machine}.\nOriginal error: {str(e)}")
            log_event(msg, "FATAL")
            raise OSError(msg)
    
    def _convert_response(
        self,
        data: dict
    ) -> GeoFoxResponse:
        """Converts JSON Response to its own dataclass
        which is defined in common/typing.py

        Args:
            data (dict): Response object

        Returns:
            GeoFoxResponse: GeoFoxResponse dataclass
        """
        try:
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
        except RuntimeError as e:
            log_event(f"HVV API has drastically changed and cannot be converted"
                      f"into GeoFoxResponse\nOriginal error: {str(e)}", "ERROR")
            return GeoFoxResponse(
                returnCode="NOT OK",
                time=GeoFoxTime("", ""),
                departures=[]
            )
    
    def _parse_geofox_data(
        self,
        rsp: GeoFoxResponse
    ) -> List[BusArrival]:
        """Parse GeoFox API response data into a list of bus arrivals.
        
        This method extracts departure information from a GeoFox response object
        and converts it into BusArrival objects, adjusting times based on the
        offset provided by the API and calculating delays.
        
        Args:
            rsp (GeoFoxResponse): The GeoFox response object containing departure data.
        
        Returns:
            List[BusArrival]: A list of BusArrival objects with line number, destination,
                                arrival time, and delay information.
        """
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
    
    @log_decorator("Sending request to HVV GeoFox")
    def get_geofox_response(self) -> GeoFoxResponse:
        """Returns the converted GeoFox API response for the
        arriving bus lines at your bus station

        For more detail, check the functions inside

        Returns:
            GeoFoxResponse: GeoFox API response
        """
        rsp = None
        try:
            rsp = self.session.request(
                method="POST",
                url=self.GEOFOX_URL,
                json=self.geofox_payload
            ).json()
            return self._convert_response(data=rsp)
        except Exception as e:
            if rsp:
                return GeoFoxResponse(
                    returnCode=rsp["returnCode"],
                    time=dacite.from_dict(data_class=GeoFoxTime, data=rsp["time"]),
                    departures=[]
                )
            else:
                log_event(f"No response from HVV GeoFox. Can't return bus times.\nException: {e}")
                return GeoFoxResponse("NOT OK", GeoFoxTime("00.00.0000", "00:00"), [])
    
    def set_bus_arrivals(self) -> None:
        if self.dh.date.hour >= self.sleep_time[0] or self.dh.date.hour < self.sleep_time[1]:
            self.sleeping = True
            log_event("No bus arrivals (Sleeping...)")
            return
        else:
            self.sleeping = False
            log_event("Getting bus arrivals...")
        
        
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