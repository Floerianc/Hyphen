import time
from typing import TYPE_CHECKING
from core.hvv import HVV

if TYPE_CHECKING:
    from app import (
        WeatherAgent,
        DateHandler,
    )

def refresh_ui(w: 'WeatherAgent', d: 'DateHandler'):
    while True:
        w.__init__(d)
        time.sleep(60)

def refresh_time(d: 'DateHandler'):
    while True:
        d.update_datetime()
        time.sleep(0.5)

def refresh_busses(hvv: HVV) -> None:
    while True:
        hvv.set_bus_arrivals()
        time.sleep(20)