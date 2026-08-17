#!/usr/bin/env python
# Program entirely written by github.com/Floerianc
# +++ Run as root! +++

__version__ = "5.0.1"

# external imports
import math
import os
import time
import traceback
import threading
from dotenv import load_dotenv
from typing import (
    Callable,
    List,
)

load_dotenv()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# local imports
from core.dawum import DAWUM
from core.enums import *
from core.canvas import Matrix
from core.visuals import *
from core.dates import DateHandler
from core.weather import WeatherAgent
from core.pollen import DWDPollen
from core.hvv import HVV
from core.holidays import Holidays
from common.logger import (
    log_event,
    log_decorator
)
from common.typing import (
    Box,
    StopableThread
)
from tests import pretty_tests
from widgets.RainBar import RainBar
from widgets.MatrixGraph import MatrixGraph

def error_exit_routine(exc: BaseException) -> None:
    log_event(
        msg="Uncaught Exception crashed the program.",
        _level="CRITICAL"
    )
    formatted_exc = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(formatted_exc)
    log_event(msg=formatted_exc, _level="CRITICAL")

def thread_exc_handler(args):
    error_exit_routine(args.exc_value)

threading.excepthook = thread_exc_handler

class Hyphen(Matrix):
    @log_decorator("Initializing Program...")
    def __init__(self, *args, **kwargs):
        """
        __init__ Initializes the LED-Panels Canvas and its functions
        """
        # Inheritance init
        super(Hyphen, self).__init__(*args, **kwargs)

        # Important classes
        self.date_handler = DateHandler()
        self.weather = WeatherAgent(self.date_handler)
        self.hvv = HVV(self.date_handler)
        self.pollen = DWDPollen()
        self.holidays = Holidays(self.date_handler)
        self.dawum = DAWUM()

        # Threads
        self.dt_thread = StopableThread(
            interval=0.5,
            target=self.date_handler.update_datetime,
            daemon=True,
        )
        self.weather_thread = StopableThread(
            interval=60,
            target=self.weather.update,
            daemon=True,
        )
        self.hvv_thread = StopableThread(
            interval=(15, 45),
            target=self.hvv.set_bus_arrivals,
            daemon=True,
        )
        self.holidays_thread = StopableThread(
            interval=3600,
            target=self.holidays.update,
            daemon=True
        )
        self.dawum_thread = StopableThread(
            interval=3600,
            target=self.dawum.update,
            daemon=True
        )

        self.dt_thread.start()
        self.weather_thread.start()
        self.hvv_thread.start()
        self.holidays_thread.start()
        self.dawum_thread.start()

        self.welcome_message = f"""
        Welcome to my LED Panel program.
        (Author: https://github.com/Floerianc)
        
        You are currently running the Version {__version__}.
        
        To run this you really need a stable WiFi connection.
        Have fun :)
        """

    def run(self) -> None:
        schedule: List[Callable] = [
            self.render_barometer_page,
            self.render_weather_page,
            self.render_bus_page,
            self.render_pollen_page,
            self.render_holiday_page,
        ]
        timer = 20.0
        idx = 0
        current_func = schedule[idx]
        switch_time = time.monotonic() + timer

        self.canvas = self.matrix.CreateFrameCanvas()
        while True:
            now = time.monotonic()
            if now >= switch_time:
                idx = (idx + 1) % len(schedule)
                current_func = schedule[idx]
                switch_time = now + timer

            self.canvas.Clear()
            self.render_info_bar()
            current_func()

            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_info_bar(self) -> None:
        # draw box
        self.draw_box(x1=0, x2=64, y1=25, y2=33, color=CLR_WHITE)

        # clock string (in box)
        self.draw_text(
            x=1,
            y=31,
            color=CLR_BLACK,
            text=self.date_handler.clock_string,
            char_width=4,
            char_height=6,
        )

        # temperature string
        self.draw_text(
            x=36,
            y=31,
            color=CLR_BLACK,
            text=f"{self.weather.current_temperature:.2f}°C",
            char_width=4,
            char_height=6,
        )

    def render_bus_page(self) -> None:
        next_busses = self.hvv.next_busses
        if len(next_busses) > 0 and not self.hvv.sleeping:
            for idx, bus in enumerate(next_busses):
                # bus line logo
                img_start_x = 1
                img_start_y = 1 + (8 * idx)
                text_x = (img_start_x + 3) + (2 * (3 - len(str(bus.line))))
                text_y = img_start_y + 6

                self.draw_image(
                    image=HVV_LOGO_BASE, start_x=img_start_x, start_y=img_start_y
                )
                self.draw_text(
                    x=text_x,
                    y=text_y,
                    color=CLR_WHITE,
                    text=str(bus.line),
                    char_width=4,
                    char_height=6,
                )

                # destination name
                name_x = 1 + len(HVV_LOGO_BASE[0]) + 2  # 1 (margin) + length of logo + gap
                name_y = text_y
                self.draw_text(
                    x=name_x,
                    y=name_y,
                    color=CLR_WHITE,
                    text=bus.destination.replace(" ", "")[0:5],
                    char_width=4,
                    char_height=6,
                )

                # time of arrival
                arrival_x = name_x + 20 + 2  # 12 = length of destination text, 1 = gap
                arrival_y = name_y
                self.draw_text(
                    x=arrival_x,
                    y=arrival_y,
                    color=CLR_CYAN,
                    text=bus.time.strftime("%H:%M"),
                    char_width=4,
                    char_height=6,
                )

                # delay
                # delay_x = arrival_x + 20 + 1  # 20 = length of time of arrival text, 1 = gap
                # delay_y = arrival_y
                # delay_minutes = round(bus.delay.seconds / 60)
                # delay_clr = CLR_GREEN if delay_minutes <= 0 else CLR_RED
                # self.draw_text(
                #     x=delay_x,
                #     y=delay_y,
                #     color=delay_clr,
                #     text=f"+{delay_minutes}",
                #     char_width=4,
                #     char_height=6,
                # )
        elif self.hvv.sleeping:
            self.draw_text(
                x=2,
                y=16,
                color=CLR_RED,
                text="Schlafenszeit:)",
                char_width=4,
                char_height=6
            )
        else:
            self.draw_text(
                x=2,
                y=16,
                color=CLR_RED,
                text="Keine Busrouten",
                char_width=4,
                char_height=6
            )

    def render_news_page(self) -> None:
        pass

    def render_pollen_page(self) -> None:
        sev = self.pollen.get_n_pollen(4)
        
        self.draw_text(
            x=19,
            y=0 + 6,
            color=CLR_WHITE,
            text="Pollen",
            char_width=4,
            char_height=6
        )

        positions: List[Box] = [
            Box(x1=1, x2=29, y1=10, y2=15),
            Box(x1=1, x2=29, y1=17, y2=22),
            Box(x1=35, x2=63, y1=10, y2=15),
            Box(x1=35, x2=63, y1=17, y2=22),
        ]

        for idx, severity in enumerate(sev.items()):
            if idx >= len(positions):
                break
            box = positions[idx]

            pollen = severity[0]
            pollen_severity = severity[1]
            letters = len(pollen) if len(pollen) < 8 else 7  # name of pollen

            if idx < round(len(positions) / 2): # if we are on the first half of positions, we're on the left side
                x = box.x1 + ((7 - letters) * 4)
            else:  # right side
                x = box.x1
            y = box.y2
            
            self.draw_text(
                x=x,
                y=y,
                color=pollen_severity.color,
                text=pollen[:letters],
                char_width=4,
                char_height=6,
            )

    def render_holiday_page(self) -> None:
        # header = "Ferientage"
        char_width = 4
        char_height = 6
        
        next_holidays = self.holidays.next_n_holidays(3)
        max_chars = 8
        
        table = self.get_table(
            x=0,
            y=0,
            rows=3,
            columns=3,
            col_width=[32, 16, 12],
            col_height=7
        )
        
        self.draw_table(
            table=table,
            color=CLR_CLOUD_1
        )
        
        for idx, holiday in enumerate(next_holidays):
            name = holiday.name if len(holiday.name) <= max_chars else holiday.name[:max_chars]
            if holiday.duration.days < 10:
                duration = f" {holiday.duration.days}d"     # added a space so the "d" (days) is aligned
            else:
                duration = f"{holiday.duration.days}d"
            
            naive_date = self.date_handler.date.replace(tzinfo=None)
            time_until = holiday.start - naive_date
            free_spaces = (table.get_width(1) // 4) - len(str(time_until.days)) - 1 # 4 = char_width; -1 = the "d" after the day amount
            time_until = " " * free_spaces + f"{time_until.days}d"
            
            self.set_table_col(
                text=name,
                row=idx,
                column=0,
                table=table,
                color=CLR_CYAN,
                char_width=char_width,
                char_height=char_height
            )
            
            self.set_table_col(
                text=time_until,
                row=idx,
                column=1,
                table=table,
                color=CLR_RED,
                char_width=char_width,
                char_height=char_height
            )
            
            self.set_table_col(
                text=duration,
                row=idx,
                column=2,
                table=table,
                color=CLR_GREEN,
                char_width=char_width,
                char_height=char_height
            )
            
            if current_holiday := self.holidays.current_holiday():
                max_chars = 15
                remaining_days = math.ceil((current_holiday.end.timestamp() - self.date_handler.date.timestamp()) / 86400) + 1 # <-- include current day
                remaining_str = f"({remaining_days}d)"
                holiday_chars = max_chars - len(remaining_str)
                if len(current_holiday.name) > holiday_chars:
                    holiday_str = "".join([current_holiday.name[0:holiday_chars-1],"-"])
                else:
                    holiday_str = current_holiday.name
                
                self.draw_box(x1=0, y1=25, x2=64, y2=32, color=CLR_GREEN)
                self.draw_text(x=2, y=31, color=CLR_BLACK, text=f"{holiday_str}{remaining_str}", char_width=4, char_height=6) # type: ignore

    def render_weather_page(self) -> None:
        # draw weather icon
        weather_image, clr = WMO_MAP.get(self.weather.weather_code, ([], ()))
        del clr

        self.draw_image(image=weather_image, start_x=1, start_y=15)

        # draw rain bar
        rain_bar = RainBar(
            canvas=self.canvas,
            x_pos=1,
            y_pos=1,
            width=8,
            height=12,
            color=CLR_FOG
        )
        rain_bar.draw_bar(
            canvas=self.canvas,
            precipitation=self.weather.precipitation,
            font_path=self.interpret_font_size(4, 6),
        )

        precipitation_graph = MatrixGraph(
            canvas=self,
            x=30,
            y=1,
            width=33,
            height=11,
            max_value=None,
            graph_color=CLR_BRIGHTER_BLUE,
            data=self.weather.precipitation_forecast(6),
        )
        precipitation_graph.render()

        temperature_graph = MatrixGraph(
            canvas=self,
            x=30,
            y=13,
            width=33,
            height=11,
            max_value=None,
            graph_color=CLR_SUN,
            data=self.weather.temperature_forecast(6),
        )
        temperature_graph.render()
    
    def render_barometer_page(self) -> None:
        # Render Title
        if not self.dawum.latest_survey:
            return
        
        parliament = self.dawum.latest_survey.Parliament
        max_length = 15
        text = parliament[:max_length]
        char_width = 4
        
        x = round(((2 + (max_length * char_width)) - (char_width * len(text))) / 2)
        
        self.draw_text(
            x=x,
            y=6,
            color=CLR_WHITE,
            text=text,
            char_width=4,
            char_height=6
        )
        
        # Render Graph
        
        party_values = [float(value) for value in self.dawum.latest_survey.Results.values()]
        
        voting_graph = MatrixGraph(
            canvas=self,
            x=9, # 2,
            y=6,
            width=54,# 60,
            height=18,
            max_value=int(max(party_values)),
            graph_color=self.dawum.get_colors(self.dawum.latest_survey),
            data=party_values
        )
        voting_graph.render()


if __name__ == "__main__":
    pretty_tests()

    app = Hyphen()
    print(app.welcome_message)

    try:
        app.process()
    except BaseException as exc:
        error_exit_routine(exc)

""" TODO
    Clean Structure of the project                                                      (X)
        - DateHandler in its own file                                                   (X)
        - WeatherHandler in its own file                                                (X)
        - Clean up code                                                                 (X)
            - Fixed Type Hinting                                                        (X)
        - Update documentation                                                          (X)
        - Fix typing errors                                                             (X)
        - Turn Hyphen class into two components, the App itself and the Canvas          (X)
            - Create own Framework. Don't use Samplebase due to complex inheritance     (X)
    Create a new structure for widgets                                                  (CANCELLED)
        - Create a Widget class                                                         (CANCELLED)
            - Should overwrite everything below it                                      (CANCELLED)
            - Custom background color (transparent = lets things below it render)       (CANCELLED)
    Fix Image dataclass                                                                 (X)
        - Turned the Image declaration into a viable dataclass                          (X)
        - Overwrite "List[List[Pixel]] with Image type hint                             (X)
    Fix Color dataclass                                                                 (X)
        - Turned the Color declaration into a viable dataclass                          (X)
        - Overwrite "tuple" with Color type hint                                        (X)
    Commit to the new UI idea                                                           (X)
        - Make rough ideas in Paint.NET or smth                                         (X)
            - Weather page                                                              (X)
            - News page                                                                 (IN PROGRESS...)
            - Bus line page                                                             (X)
                - HVV Logo                                                              (X)
                - Bus lines                                                             (X)
                - Time of arrival                                                       (X)
                - Delay                                                                 (X)
            - Pollen page                                                               (X)
            - Untis page                                                                (X)
            - Feiertage und Ferien page                                                 (X)
            - Politikbarometer                                                          (X)
        - Build new UI                                                                  (X)
            - Weather page                                                              (X)
                - Lower box with time and temperature                                   (X)
                - Weather icon                                                          (X)
                - Raindrop icon                                                         (X)
                - Rain bar                                                              (X)
                - Rain forecast                                                         (X)
                - Fix visual bug with double-digits values (clips into line)            (X)
            - News page                                                                 (IN PROGRESS...)
            - Bus line page                                                             (X)
                - Found alternative for HVV API (Scraping with PlayWright)              (X)
                - Creating Logos/Visuals for the display                                (X)
                - Drawing all components to the screen                                  (X)
                - PlayWright does NOT work on Raspberry Pi 2 soooo Selentium            (X)
                    - Found work-around for chromium drivers on different OS            (X)
                - Added visual indicator if HVV does not respond                        (X)
            - Pollen page                                                               (X)
                - Show Pollen based on relevancy, not by hard coding them               (X)
                - Fixed visual bug with the name clipping out of bounds                 (X)
            - Untis page                                                                (IN PROGRESS...)
            - Ferien und Feiertage                                                      (X)
                - Maybe try a table-style display?                                      (X)
                    Okay, Tables are much more difficult than I thought
                    - Use one big box and then draw lines instead of only draw_box      (X)
                - Added a container to show current holiday / vacation                  (X)
                - Made the text black for more contrast                                 (X)
            - Politikbarometer                                                          (X)
    Converter for images instead of large pixel matrices                                (X)
        - Built converter from .png to pixels                                           (X)
        - Fixed file path problem                                                       (X)
        - Remove .pixel_matrix implementation. Instead use inheritance                  (X)
    Fix 24/7 Problem                                                                    (X)
        - Switch through windows/pages                                                  (X)
        - Fix weather requests on 12 am                                                 (FIX?)
            - I guess I solved it by not using the function causing it anymore          (X)
            Now sometimes the weather data just doesn't load at all.                    (FIX?)
                No Weather data from OpenMeteo? Try OpenMeteo implementation instead    (X)
        - HVV doesn't return "departures" sometimes, do better error handling           (X)
        - Weather data does not update in real-time                                     (X)
            Problem description:
                After 12am the hour index sets back to 0 which gets the
                items from the same day because it does not update properly
                although it requests new data every 60 seconds on another thread and
                the ID of the response also changes so obviously the data is new and
                changes frequently but still wraps around to the same day
            Solution:
                Ig what saved it is not relying on a cache by openmeteo because
                then it will never update.
                I also changed the way the temperature and percipitance is handled
                because now depending on the method it will either use the hourly
                forecast by openmeteo or the current weather data provided by openmeteo
    Optimization:                                                                       (X)
        - Optimize Selenium options                                                     (X)
        - Research if other browsers are faster                                         (X)
            - Ig there's Htmlunit, but its not supported in the Python bindings?        (X)
    Alternative for Selenium                                                            (X)
        - Use GeoFox API instead                                                        (X)
            - Get API URL from Fetch response in Network Tab (F12)                      (X)
            - Copy Headers and payload from POST request                                (X)
            - Read what the response keys mean                                          (X)
                - (https://gti.geofox.de/pdf/GEOFOX_GTI_Anwenderhandbuch_p.pdf Page 41) (X)
                - You can find this by searching for 'site:gti.geofox.de "timeOffset"'  (X)
        - Create typing for all GeoFox API related objects I use                        (X)
            - GeoFoxResponse,Departure,DepartureLine,DepartureStation,DepartureLineType (X)
            - Created a converter for the JSON response to the dataclass                (X)
        - Find a way to include delay (for some reason missing?)                        (X)
    Workflow for exiting                                                                (X)
        - Clean exit for CRTL-C but still error traceback                               (X)
    HUGE PROBLEM: Can't deploy on Raspberry Pi 3                                        (FIX)
        Can't compile Numpy and Pandas                                                  (FIX)
        rgbmatrix.core does not exist                                                   (FIX)
        Instead of using different venv each time just update one specific venv         (FIX)
        Fixed Sudo problems                                                             (FIX)
        No module named "idna.uts46data"                                                (FIX?)
            - Fixed with the sudo-only approach
        No module named "numpy.full"                                                    (FIX)
        No module named "pygame.rect"                                                   (FIX)
        No permission for .cache                                                        (FIX)
        Can't assign canvas width and height                                            (FIX)
        HVV does not return anything                                                    (FIX?)
            - Fixed with the sudo-only approach
        Can't find Font assets                                                          (FIX)
        Selenium does not run at all                                                    (FIX?)
            - Fixed with the sudo-only approach
        urllib3 can't use HTTP                                                          (FIX?)
            - Fixed with the sudo-only approach
        New foundings:
            1. Tests.py work but app.py doesn't                                         (FIX)
            2. The problem is line 197 in core/hvv.py                                   (FIX?)
                - Fixed with the sudo-only approach
            3. maybe its the certifi cert (error message does not appear in tests)      (FIX?)
                - Fixed with the sudo-only approach
        Create Tests for the Raspberry Pi 3 deployment                                  (X)
            Check permissions                                                           (X)
            Check installed packages                                                    (X)
            Test Weather cache                                                          (X)
            Test imports                                                                (X)
            Test rgbmatrix                                                              (X)
            Test HVV response                                                           (X)
            Test fonts                                                                  (X)
            Test DAWUM                                                                  (X)
            Test Proxy                                                                  (X)
    EVEN MORE FUCKING FLICKERING WOOOOO                                                 (X)
        Rework the FUCKING Core again                                                   (Actually nah)
            Canvas.py                                                                   (X)
                Draw box and image                                                      (X)
        Is it smoother with the original samplebase.py instead of my implementation?    (X)
            Yes.                                                                        (X)
            So, apparently I have implemented it weirdly and now it works               (X)
    Added a cool little start-up checkup lol                                            (X)
    Untis Integration                                                                   (IN PROGRESS...)
        - Ask Untis support for help with integration because how tf                    (IN PROGRESS...)
    Weather Page update                                                                 (X)
        - Added graphs for temperature and precipitation                                (X)
        - Added common MatrixGraph class                                                (X)
            - Big class for re-usable graphs on the RGBMatrix                           (X)
    Log Clean-up                                                                        (X)
        - Better error handling (Different levels, not just DEBUG and INFO)             (X)
        - Clean-up INFO and DEBUG logs every 24 hrs.                                    (X)
        - Clean-up after every restart                                                  (X)
    Modernize threading process                                                         (X)
        - Use Asyncio instead                                                           (CANCELLED)
        - Instead, using StopableThread (typing.py) now                                 (X)
    Uptime monitor                                                                      (NOT STARTED YET)
    Convert to .env                                                                     (X)
    Compress isinstance() calls to one line in canvas.py                                (X)
    Create an actually decent README.md lol                                             (IN PROGRESS...)
    Avoid HVV IP Ban :(                                                                 (X)
        5 Stage Scraper:                                                                (IN PROGRESS...)
            1. Identity masking (Disguise as Browser)                                   (X) <-- RequestWrapper
            UA: https://explore.whatismybrowser.com/useragents/explore/
            2. Randomized interval between requests                                     (X) <-- Threads choose random interval
            3. Sleep between 10pm - 5am                                                 (X) <-- hvv.py disallows requests, might move over to requestwrapper
            4. Proxy rotation                                                           (IN PROGRESS...)
                - Build integration for own proxies                                     (IN PROGRESS...)
                - Build integration for Decodo paid proxies                             (IN PROGRESS...)
                https://decodo.com/blog/mastering-python-requests/                      (IN PROGRESS...)
            5. Random Retrying (different Headers, Proxies etc.)                        (X)
        Create a class which is a wrapper or overhead requests class so proxies shared  (X)
            - Allow for dynamic payloads. They're not static but can be changed by user (X)
            - Replace requests with RequestWrapper in classes that scrape               (X)
    DAWUM Implementation                                                                (X)
        - Correctly center the Parliament title                                         (X)
        - Maybe change a few colors so it's easy to distinguish or add text labels on x (X)
        - Show max percentage of party like in the weather graphs                       (X)
        - Fuck classes lmao just make it a function for no reason                       (X)
            - Turned it into a class again award                                        (X)
        - Make it so it only shows up until 5% and Others because who cares             (X)
            - Show others                                                               (X)
            - Show only up until 5%                                                     (X)
        - Add color coded parties                                                       (X)
            - Rewrite MatrixGraph                                                       (X)
        - Only show Bundestag                                                           (X)
        - Maybe add optional flags for certain states                                   (X)
        - Maybe remove the FormattedSurvey class and just format immediately            (X)
    - Force "Schlafenszeit" screen when in Schlafenszeit instead of showing old rsp     (X)
    - Fix display for "Ambrosia" (one shifted to the left and not aligned anymore)      (X)
    - Show remaining days of current vacation / holiday.                                (X)
    - Create running text                                                               (X)
    - Fixed the order of the parties in the barometer page so "Sonstige" is always last (X)
    
    Long-term ideas:
        Create a page system
        Create a GUI to create own pages
        Add schedule to a config file
        Disable pages through command line arguments
"""