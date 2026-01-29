import time
from core.hvv import HVV
from core.weather import WeatherAgent
from core.dates import DateHandler

def refresh_ui(w: WeatherAgent) -> None:
    while True:
        w.update()
        time.sleep(60)

def refresh_time(d: DateHandler) -> None:
    while True:
        d.update_datetime()
        time.sleep(0.5)

def refresh_busses(hvv: HVV) -> None:
    while True:
        hvv.set_bus_arrivals()
        time.sleep(20)