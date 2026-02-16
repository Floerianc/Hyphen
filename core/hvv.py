import platform
import requests
import dacite
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
        """Header for the GeoFox API

        Returns:
            dict: HTTP Header
        """
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
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
            "maxList": 10,
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
        return datetime(now.year, now.month, now.day, int(hour), int(minute), now.second)

    @log_event("Getting arrivals list...")
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
        """Converts JSON Response to its own dataclass
        which is defined in common/typing.py

        Args:
            data (dict): Response object

        Returns:
            GeoFoxResponse: GeoFoxResponse dataclass
        """
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
    
    @log_event("Sending request to HVV GeoFox")
    def get_geofox_response(self) -> GeoFoxResponse:
        """Returns the converted GeoFox API response for the
        arriving bus lines at your bus station

        For more detail, check the functions inside

        Returns:
            GeoFoxResponse: GeoFox API response
        """
        rsp = None
        try:
            rsp = requests.post(
                url=self.GEOFOX_URL,
                headers=self.geofox_header,
                json=self.geofox_payload,
                timeout=20
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