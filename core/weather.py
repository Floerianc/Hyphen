import requests
from os import environ
from datetime import (
    timedelta,
    timezone,
    datetime
)
from typing import (
    Optional,
    List,
    Union,
)
from core.dates import DateHandler
from common.logger import log_event
from common.typing import Weather


class WeatherAgent:
    def __init__(
        self,
        date: DateHandler
    ) -> None:
        self.date_handler = date
        self.max_forecast_hours = 6
        
        # self.session = requests_cache.CachedSession(
        #     cache_name='.cache',
        #     expire_after=180
        # )
        # self.retry_session = retry(
        #     self.session,
        #     retries=5,
        #     backoff_factor=0.2
        # )
        # self.openmeteo = openmeteo_requests.Client(session=self.retry_session
        
        self.session = requests.Session()
        self.data = self._fetch_weather()

    def _fetch_weather(self) -> Optional[Weather]:
        """Returns the "Hourly" data of the Weather API

        Returns:
            Optional[VariablesWithTime]: Variables from Openmeteo
        """
        url = environ.get("WEATHER_URL", "")
        params = {
            "latitude": float(environ.get("WEATHER_LATITUDE", "")),
            "longitude": float(environ.get("WEATHER_LONGITUDE", "")),
            "hourly": ["temperature_2m", "precipitation_probability", "precipitation"],
            "current": ["temperature_2m", "weather_code", "precipitation"],
            "timezone": environ.get("WEATHER_TIMEZONE", ""),
            "forecast_days": 1,
            "timeformat": "unixtime",
        }
        try:
            r = self.session.get(url, params=params, timeout=15)
            r.raise_for_status()
            return Weather._from_dict(r.json())
        except Exception as e:
            log_event(f"Weather API request failed: {str(e)}")
            return None
    
    def update(self) -> None:
        new_data = self._fetch_weather()
        if new_data is not None:
            self.data = new_data
        # print(self.session.cache.urls())
        # print(str(self.session.cache.responses))
    
    @property
    def hourly_variable_len(self) -> int:
        if self.data:
            temps = self.data.hourly.temperature_2m
            if temps:
                return len(temps)
            else:
                log_event("No temperature data", "WARN")
                return -1
        else:
            log_event("Weather data is not set.", "WARN")
            return -1
    
    @property
    def hour_index(self) -> int:
        """Returns the current hour. Useful for selecting
        an item in a list

        Returns:
            int: Current hour
        """
        if self.data:
            utc_date = self.date_handler.date.astimezone(timezone.utc)
            utc_data_start = datetime.fromtimestamp(self.data.hourly.time[0], timezone.utc)
            time_delta: timedelta = utc_date - utc_data_start
            index = int(time_delta.total_seconds()) // (60**2)
            return max(0, min(index, self.hourly_variable_len))
        else:
            # fallback
            log_event("Weather data is not set.", "WARN")
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
            try:
                return self.data.current.temperature_2m
            except (IndexError, ValueError):
                log_event("Couldn't find the current temperature", "ERROR")
                raise RuntimeError("No temperature available")
        else:
            log_event("Couldn't find any weather data", "ERROR")
            raise RuntimeError("Weather data is not available")
    
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
            probs = self.data.hourly.precipitation_probability
            start = self.hour_index
            
            if len(probs) == 0:
                log_event(f"No rain probabilities available", "ERROR")
                raise RuntimeError("No rain probability data")
            
            end = min(start + self.max_forecast_hours, len(probs))
            window = probs[start:end]
            
            return self.average(window)
        else:
            log_event("Couldn't find any weather data", "ERROR")
            raise RuntimeError("Weather data is not available")

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
            prec = self.data.hourly.precipitation
            start = self.hour_index
            
            if len(prec) == 0:
                log_event(f"No rain precipitation available", "ERROR")
                raise RuntimeError("No rain precipitation data")
            
            end = min(start + hours, len(prec))
            return [float(p) for p in prec[start:end]]
        else:
            log_event("Couldn't find any weather data", "ERROR")
            raise RuntimeError("Weather data is not available")
    
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
            temps = self.data.hourly.temperature_2m
            start = self.hour_index
            
            if len(temps) == 0:
                log_event(f"No temperatures available", "ERROR")
                raise RuntimeError("No temperature data")
            
            end = min(start + hours, len(temps))
            return [float(t) for t in temps[start:end]]
        else:
            log_event("Couldn't find any weather data", "ERROR")
            raise RuntimeError("Weather data is not available")

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
            try:
                return self.data.current.precipitation
            except (IndexError, ValueError):
                log_event(f"Couldn't find precipitation.", "ERROR")
                raise RuntimeError("No rain data")
        else:
            log_event("Couldn't find any weather data", "ERROR")
            raise RuntimeError("Weather data is not available")

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
            try:
                return self.data.current.weather_code
            except (IndexError, ValueError):
                log_event(f"Couldn't find weather code", "ERROR")
                raise RuntimeError("No weather code data")
        else:
            log_event("Couldn't find any weather data", "ERROR")
            raise RuntimeError("Weather data is not available")

    # @property
    # def weather(self) -> Tuple[Image, Color]:
    #     code = self.weather_code
    #     if code != -1:
    #         return WMO_MAP.get(code, (IMG_SUN, CLR_SUN))
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
                "Couldn't calculate average: no weather data available",
                "ERROR"
            )
            return -1