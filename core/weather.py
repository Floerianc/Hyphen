import requests_cache
import openmeteo_requests
from numpy import ndarray
from openmeteo_sdk.VariablesWithTime import VariablesWithTime
from retry_requests import retry
from typing import (
    Optional,
    List,
    Union,
    Tuple,
)
from core.visuals import (
    Pixel,
    IMG_SUN,
    CLR_SUN,
    CLR_RED,
)
from core.enums import WMO_MAP
from core.dates import DateHandler
from common.typing import (
    Color,
    Image,
)
from common.logger import log_event


class WeatherAgent:
    def __init__(
        self,
        date: DateHandler
    ) -> None:
        self.date_handler = date
        self.max_forecast_hours = 6
        
        self.session = requests_cache.CachedSession(
            cache_name='.cache',
            expire_after=3600
        )
        self.retry_session = retry(
            self.session,
            retries=5,
            backoff_factor=0.2
        )
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        
        self.data = self._fetch_weather()

    def _fetch_weather(self) -> Optional[VariablesWithTime]:
        """Returns the "Hourly" data of the Weather API

        Returns:
            Optional[VariablesWithTime]: Variables from Openmeteo
        """
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 53.55,
            "longitude": 9.9333,
            "hourly": [
                "temperature_2m",
                "precipitation_probability",
                "precipitation",
                "weather_code"
            ],
            "models": "best_match",
            "timezone": "auto",
            "forecast_days": 1,
            "timeformat": "unixtime",
        }
        try:
            rsps = self.openmeteo.weather_api(url, params=params)
            rsp = rsps[0]
            return rsp.Hourly()
        except Exception as e:
            log_event(f"Weather API request failed: {str(e)}")
            return None
    
    def update(self) -> None:
        new_data = self._fetch_weather()
        if new_data:
            self.data = new_data
    
    @property
    def hour_index(self) -> int:
        """Returns the current hour. Useful for selecting
        an item in a list

        Returns:
            int: Current hour
        """
        return self.date_handler.date.hour
    
    @property
    def current_temperature(self) -> float:
        """Returns the current temperature

        If it fails, it will log an error into
        the log file. Also, if the API returns
        an empty list, it will just return -100
        or -200 if there is no data to begin with.

        Returns:
            float: Current temperature
        """
        if self.data:
            temps = self.data.Variables(0).ValuesAsNumpy()  # type: ignore
            try:
                return float(temps[self.hour_index])
            except (IndexError, ValueError) as e:
                log_event(str(e))
                return -100
        else:
            return -200
    
    @property
    def rain_forecast_avg(self) -> Union[int, float]:
        """Returns the average rain forcast probability for the next hours.

        The method may fail if the API does not return
        data or is not assigned. In that case, the method
        will return -1 instead.

        Returns:
            Union[int, float]: Average rain forcast probability
        """
        if self.data:
            probs: ndarray = self.data.Variables(1).ValuesAsNumpy()  # type: ignore
            start = self.hour_index
            
            if probs.size == 0 or start < 0:
                return -1
            
            end = min(start + self.max_forecast_hours, len(probs))
            window = probs[start:end]
            
            return self.average(list(window))
        else:
            return -1

    def precipitation_forecast(
        self,
        hours: int
    ) -> List[float]:
        """Returns the amount of precipitation in mm for
        the next `x` hours.
        
        If the method fails, for example due to an error
        with the API, it will return an empty list

        Args:
            hours (int): The amount of hours into the future

        Returns:
            List[float]: Precipitation forecast in mm
        """
        if self.data:
            prec: ndarray = self.data.Variables(2).ValuesAsNumpy()  # type: ignore
            start = self.hour_index
            
            if prec.size == 0 or start < 0:
                log_event(f"{prec}, {start}")
                return []
            
            end = min(start + hours, len(prec))
            return [float(p) for p in prec[start:end]]
        else:
            return []
    
    def temperature_forecast(
        self,
        hours: int
    ) -> List[float]:
        """Returns the temperature in celsius for the next
        `x` hours.
        
        If the method fails, for example due to an error
        with the API, it will return an empty list

        Args:
            hours (int): The amount of hours into the future

        Returns:
            List[float]: Temperature forecast in celsius
        """
        if self.data:
            temps: ndarray = self.data.Variables(0).ValuesAsNumpy() # type: ignore
            start = self.hour_index
            
            if temps.size == 0 or start < 0:
                log_event(f"{temps}, {start}")
                return []
            
            end = min(start + hours, len(temps))
            return [float(t) for t in temps[start:end]]
        else:
            return []

    @property
    def precipitation(self) -> float:
        """Returns the current precipitation in mm

        If the API returns nothing, it
        will just return 0.0 or -1.0 if there
        is no data to begin with.

        Returns:
            float: Current precipitation in mm
        """
        if self.data:
            prec = self.data.Variables(2).ValuesAsNumpy()  # type: ignore
            try:
                return float(prec[self.hour_index + 1])
            except (IndexError, ValueError):
                return 0.0
        else:
            return -1.0

    @property
    def weather_code(self) -> int:
        """Returns the weather code for the current weather

        If the API returns nothing, it
        will just return -1 or -2 if there
        is no data to begin with.

        Returns:
            float: Current precipitation in mm
        """
        if self.data:
            codes = self.data.Variables(3).ValuesAsNumpy()  # type: ignore
            try:
                return int(codes[self.hour_index])
            except (IndexError, ValueError):
                return -1
        else:
            return -2

    # @property
    # def weather(self) -> Tuple[Image, Color]:
    #     code = self.weather_code
    #     if code != -1:
    #         return WMO_MAP.get(code, (IMG_SUN, CLR_SUN))  # type: ignore
    #     return ([[Pixel(True)]], CLR_RED)

    def average(
        self,
        values: List[Union[int, float]]
    ) -> Union[int, float]:
        """Returns the average for a given list
        of int and/or floats.
        
        The method might return -1 if the length of
        the list is equal to 0 due to the
        `ZeroDivisionError`.

        Args:
            values (List[Union[int, float]]): List of ints/floats

        Returns:
            Union[int, float]: Average
        """
        try:
            return sum(values) / len(values)
        except ZeroDivisionError:
            log_event(
                "Couldn't calculate average: no weather data available"
            )
            return -1