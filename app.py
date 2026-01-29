#!/usr/bin/env python
# Program entirely written by github.com/Floerianc 
# +++ Run as root! +++

__version__ = "3.2.2"

# external imports
import os
import time
from threading import Thread
from typing import (
    Callable,
    List,
)

os.chdir(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)

# local imports
import core.threads as threads
import core.hvv as hvv
from core.enums import *
from core.canvas import Matrix
from core.visuals import *
from core.dates import DateHandler
from core.weather import WeatherAgent
from core.pollen import DWDPollen
from common.logger import log_event
from common.typing import Box
from widgets.RainBar import RainBar
from widgets.PrecipitationForecast import PrecipitationForecastWidget

# sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

class Hyphen(Matrix):
    @log_event("Initializing Program...")
    def __init__(self, *args, **kwargs):
        """
        __init__ Initializes the LED-Panels Canvas and its functions
        """
        # Inheritance init
        super(Hyphen, self).__init__(*args, **kwargs)
        
        # Important classes
        self.date_handler = DateHandler()
        self.weather = WeatherAgent(self.date_handler)
        self.hvv = hvv.HVV(self.date_handler)
        self.pollen = DWDPollen()

        # Threads
        self.dt_thread = Thread(target=threads.refresh_time, args=[self.date_handler,], daemon=True)
        self.weather_thread = Thread(target=threads.refresh_ui, args=[self.weather,], daemon=True)
        self.hvv_thread = Thread(target=threads.refresh_busses, args=[self.hvv,], daemon=True)

        self.dt_thread.start()
        self.weather_thread.start()
        self.hvv_thread.start()
        
        self.welcome_message = f"""
        Welcome to my LED Panel program.
        (Author: https://github.com/Floerianc)
        
        You are currently running the Version {__version__}.
        
        To run this you really need a stable WiFi connection.
        Have fun :)
        """

    # def display_message(self, msg: str, timeout_duration: int = 10) -> None:
    #     print("Displaying Message")

    #     time.sleep(0.5)
    #     self.clear()
    #     self.draw_text(1, 36, 255, 255, 255, msg, 4, 6)
    #     time.sleep(timeout_duration)
    
    def run(self) -> None:
        schedule: List[Callable] = [
            self.render_weather_page,
            self.render_bus_page,
            self.render_pollen_page,
        ]
        timer = 20.0
        idx = 0
        current_func = schedule[idx]
        switch_time = time.monotonic() + timer
        
        self.canvas = self.matrix.CreateFrameCanvas()
        while True:
            # FIXME: Very CPU expensive
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
        self.draw_box(
            x1=0,
            x2=64,
            y1=25,
            y2=33,
            color=CLR_WHITE
        )
        
        # clock string (in box)
        self.draw_text(
            x = 1,
            y = 31,
            color = CLR_BLACK,
            text = self.date_handler.clock_string,
            char_width=4,
            char_height=6
        )
        
        # temperature string
        self.draw_text(
            x = 36,
            y = 31,
            color = CLR_BLACK,
            text = f"{self.weather.current_temperature:.2f}°C",
            char_width=4,
            char_height=6
        )
    
    def render_bus_page(self) -> None:
        for idx, bus in enumerate(self.hvv.next_busses):
            # bus line logo
            img_start_x = 1
            img_start_y = 1 + (8 * idx)
            text_x = (img_start_x + 3) + (2 * (3 - len(str(bus.line))))
            text_y = img_start_y + 6
            
            self.draw_image(image=HVV_LOGO_BASE, start_x=img_start_x, start_y=img_start_y)
            self.draw_text(x=text_x, y=text_y, color=CLR_WHITE, text=str(bus.line), char_width=4, char_height=6)
            
            # destination name
            name_x = 1 + len(HVV_LOGO_BASE[0]) + 2  # 1 (margin) + length of logo + gap
            name_y = text_y
            self.draw_text(x=name_x, y=name_y, color=CLR_WHITE, text=bus.destination.strip()[0:3], char_width=4, char_height=6)
            
            # time of arrival
            arrival_x = name_x + 12 + 1 # 12 = length of destination text, 1 = gap
            arrival_y = name_y
            self.draw_text(x=arrival_x, y=arrival_y, color=CLR_CYAN, text=bus.time.strftime("%H:%M"), char_width=4, char_height=6)
            
            # delay
            delay_x = arrival_x + 20 + 1 # 20 = length of time of arrival text, 1 = gap
            delay_y = arrival_y
            delay_minutes = round(bus.delay.seconds / 60)
            delay_clr = CLR_GREEN if delay_minutes <= 0 else CLR_RED
            self.draw_text(x=delay_x, y=delay_y, color=delay_clr, text=f"+{delay_minutes}", char_width=4, char_height=6)
    
    def render_news_page(self) -> None:
        pass
    
    def render_pollen_page(self) -> None:
        self.pollen.update()
        sev = self.pollen.get_pollen_severity(["Graeser", "Birke", "Roggen", "Esche"])
        self.draw_text(x=19, y=0+6, color=CLR_WHITE, text="Pollen", char_width=4, char_height=6)
        
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
            letters = len(pollen)  # name of pollen
            
            if idx < round(len(positions) / 2): # if we are on the first half of positions, we're on the left sind
                x = box.x1 + ((7 - letters) * 4)
            else:   # right side
                x = box.x1
            y = box.y2
            self.draw_text(x=x, y=y, color=pollen_severity.color, text=pollen, char_width=4, char_height=6)
    
    def render_untis_page(self) -> None:
        pass
    
    def render_weather_page(self) -> None:
        # draw weather icon
        weather_image, clr = WMO_MAP.get(self.weather.weather_code, ([], ()))
        del clr
        
        self.draw_image(
            image=weather_image,
            start_x=1,
            start_y=15
        )
        
        # draw rain bar
        rain_bar = RainBar(
            canvas = self.canvas, 
            x_pos = 1, 
            y_pos = 1,
            width = 8, 
            height = 12, 
            color = CLR_FOG
        )
        rain_bar.draw_bar(
            canvas=self.canvas,
            precipitation=self.weather.precipitation,
            font_path=self.interpret_font_size(4, 6)
        )
        
        # draw rain icon
        rain_image = IMG_RAINDROP
        self.draw_image(
            image=rain_image,
            start_x=56,
            start_y=1
        )
        
        # draw precipitation forecast
        pfw = PrecipitationForecastWidget(
            canvas=self.canvas,
            x_pos=24,
            y_pos=7,
            font=self.interpret_font_size(4, 6),
            font_color=Color(255, 255, 255),
            gap=1,
            precipitation_forecast=self.weather.precipitation_forecast(3)
        )
        pfw.render()

if __name__ == "__main__":
    CHECK_UP = True

    if CHECK_UP:
        import tests
        tests.pretty_tests()

    app = Hyphen()
    print(app.welcome_message)

    try:
        app.process()
    except KeyboardInterrupt:
        pass


""" TODO
    Clean Structure of the project                                                      (X)
        - DateHandler in its own file                                                   (X)
        - WeatherHandler in its own file                                                (X)
        - Clean up code                                                                 (X)
        - Update documentation                                                          (NOT STARTED YET)
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
    Commit to the new UI idea                                                           (IN PROGRESS...)
        - Make rough ideas in Paint.NET or smth                                         (IN PROGRESS...)
            - Weather page                                                              (X)
            - News page                                                                 (IN PROGRESS...)
            - Bus line page                                                             (X)
                - HVV Logo                                                              (X)
                - Bus lines                                                             (X)
                - Time of arrival                                                       (X)
                - Delay                                                                 (X)
            - Pollen page                                                               (X)
            - Untis page                                                                (X)
        - Build new UI                                                                  (IN PROGRESS...)
            - Weather page                                                              (X)
                - Lower box with time and temperature                                   (X)
                - Weather icon                                                          (X)
                - Raindrop icon                                                         (X)
                - Rain bar                                                              (X)
                - Rain forecast                                                         (X)
            - News page                                                                 (IN PROGRESS...)
            - Bus line page                                                             (X)
                - Found alternative for HVV API (Scraping with PlayWright)              (X)
                - Creating Logos/Visuals for the display                                (X)
                - Drawing all components to the screen                                  (X)
                - PlayWright does NOT work on Raspberry Pi 2 soooo Selentium            (X)
                    - Found work-around for chromium drivers on different OS            (X)
            - Pollen page                                                               (X)    <---
            - Untis page                                                                (IN PROGRESS...)
    Converter for images instead of large pixel matrices                                (X)
        - Built converter from .png to pixels                                           (X)
        - Fixed file path problem                                                       (X)
    Fix 24/7 Problem                                                                    (X)
        - Switch through windows/pages                                                  (X)
        - Fix weather requests on 12 am                                                 (FIX?)
            - I guess I solved it by not using the function causing it anymore          (X)
            Now sometimes the weather data just doesn't load at all.                    (FIX?)
                No Weather data from OpenMeteo? Try OpenMeteo implementation instead    (X)
        - HVV doesn't return "departures" sometimes, do better error handling           (X)
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
"""