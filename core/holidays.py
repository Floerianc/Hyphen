from os import environ
from bs4 import BeautifulSoup
from bs4._typing import _SomeTags
from datetime import (
    datetime,
    timedelta
)
from typing import (
    List,
    Optional
)
from core.dates import DateHandler
from core.proxy import SessionWrapper
from common.typing import Holiday
from common.logger import log_event

class Holidays:
    def __init__(
        self,
        dh: DateHandler
    ) -> None:
        """Initiates the Holidays class

        This class handles most of the work with the
        holidays and vacation days in Germany and
        in a certain state.

        Args:
            dh (DateHandler): Handles the Date and Clock
        """
        self.holiday_URL = environ.get("HOLIDAY_URL", "https://get.api-feiertage.de/")
        self.vacation_URL = environ.get("VACATION_URL", "")
        
        self.date_handler = dh
        self.session = SessionWrapper(timeout=20)
        
        self.sorted_holidays = []
        self.update()
    
    @property
    def holidays(self) -> List[Holiday]:
        """Returns all Holidays from the URL in a list
        using the \"Holiday\" dataclass

        Returns:
            List[Holiday]: List of Holidays
        """
        rsp = self.session.request(
            "GET",
            url=self.holiday_URL
        ).json()
        if rsp["status"] != "success":
            log_event(
                msg="API call to the Holiday URL failed. (Status != \"success\")",
                _level="WARN"
            )
            return []
        return [
            Holiday(
                name=holiday["fname"],
                start=self._interpret_date(holiday["date"], target_format="%Y-%m-%d", target_sep="-"),
                end=self._interpret_date(holiday["date"], target_format="%Y-%m-%d", target_sep="-") + timedelta(days=1)
            ) for holiday in rsp["feiertage"]
        ]
    
    @property
    def vacations(self) -> List[Holiday]:
        """Scrapes the given website for vacations in a
        given state in Germany.

        If everything works it will return a list of 
        the vacations using the Holiday dataclass

        Returns:
            List[Holiday]: List of vacations
        """
        vacations_this_year = []
        
        for vacation in self._scrape_vacations():
            vacation_data = vacation.get("data-header") + "ferien"      # data-header attr in <div>
            dates = vacation.find("span", class_="nowrap")              # <span>
            if not dates or not vacation_data:
                log_event(
                    msg="Couldn't find date or vacation data in vacation."
                        f"D: {dates}, VD: {vacation_data}, V: {vacation}",
                    _level="WARN"
                )
                continue
            else:
                dates = map(str.strip, dates.text.split("-"))
                dates = list(map(self._interpret_date, dates))
                if len(dates) == 1:
                    dates.append(dates[0] + timedelta(days=1))
                
                try:
                    vacations_this_year.append(Holiday(
                        name=str(vacation_data),
                        start=dates[0],
                        end=dates[1]
                    ))
                except:
                    log_event(
                        msg=f"Couldn't add vacation to list. Name: {str(vacation_data)}, Dates: {str(dates)}",
                        _level="ERROR"
                    )
        return vacations_this_year
    
    @property
    def next_holidays(self) -> List[Holiday]:
        """Returns the next holidays

        Merges the holidays and vacations lists
        and then sorts them by the start date
        of the Holiday

        Returns:
            List[Holiday]: Sorted list of holidays and vacations
        """
        holidays = self.holidays
        vacations = self.vacations
        combined = holidays + vacations
        return sorted(
            combined,
            key=lambda h: h.start,
        )
    
    @property
    def is_holiday(self) -> bool:
        return isinstance(self.current_holiday(), Holiday)
    
    def _scrape_vacations(self) -> List:
        """Scrapes the vacations from the given
        website URL

        Returns:
            _SomeTags: The elements containing the vacation data
        """
        html_content = self.session.request(
            method="GET",
            url=self.vacation_URL,
        )
        
        if not html_content.status_code == 200:
            if html_content.status_code == 998:
                log_event(f"Blocked by URL \"{self.vacation_URL}\"", "FATAL")
            log_event(
                msg=f"Request to vacations URL failed. Error code: \"{html_content.status_code}\"",
                _level="ERROR"
            )
            return _SomeTags(None)
        
        soup = BeautifulSoup(html_content.text, "html.parser")
        try:
            this_year = soup.find(class_="current")
            return this_year.find_all(class_="land_ferien_termin")
        except:
            log_event(
                f"Couldn't find vacations.",
                _level="ERROR"
            )
            return _SomeTags(None)
    
    def _interpret_date(
        self,
        date: str,
        target_format: str = "%d.%m.%Y",
        target_sep: str = "."
    ) -> datetime:
        """Interprets a date as a datetime object

        You can optionally pass a target_format
        and target_sep if the date does not match
        the default format and sep

        Args:
            date (str): String containing date
            target_format (str, optional): Format of date. Defaults to "%d.%m.%Y".
            target_sep (str, optional): Seperator between date values. Defaults to ".".

        Returns:
            datetime: Datetime object
        """
        values = date.split(target_sep)
        values = list(filter(any, values))
        if len(values) == 3:
            return datetime.strptime(date, target_format)
        elif len(values) == 2:
            return datetime.strptime(f"{date}{self.date_handler.date.year}", target_format)
        else:
            return self.date_handler.date
    
    def next_n_holidays(
        self,
        n: int
    ) -> List[Holiday]:
        """Returns the next n holidays/vacations

        This merges holidays and vacations, then
        sorts them by the start date and then
        returns the next n holidays.

        Args:
            n (int): Next n holidays/vacations

        Returns:
            List[Holiday]: List of the next n holidays/vacations
        """
        holidays = self.sorted_holidays
        now = self.date_handler.date.timestamp()
        for idx, holiday in enumerate(holidays):
            # can't compare naive and aware datetime objects so
            # instead compare both timestamps
            if holiday.start.timestamp() > now:
                start = idx
                end = min(start + n, len(holidays))
                return holidays[start:end]
            else:
                continue
        return []
    
    def current_holiday(self) -> Optional[Holiday]:
        for holiday in self.sorted_holidays:
            start = holiday.start.timestamp()
            if start <= self.date_handler.date.timestamp() <= holiday.end.timestamp():
                return holiday
            if start > self.date_handler.date.timestamp():
                return None
        return None
    
    def update(self) -> None:
        holidays = self.next_holidays
        if holidays:
            self.sorted_holidays = holidays