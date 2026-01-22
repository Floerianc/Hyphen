import platform
import os
from dataclasses import dataclass
from colorama import Fore
from typing import (
    Callable,
    List
)

from core.hvv import HVV
from core.weather import WeatherAgent
from core.dates import DateHandler
from core.canvas import Matrix
from common.typing import Color
from util.utils import FONT_PATH

os.chdir(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)

@dataclass
class TestResult:
    success: bool
    msg: str

def _test_weather_cache() -> TestResult:
    OS = platform.system()
    if OS == "linux":
        path = "/tmp/weather.cache"
    else:
        path = ".cache"
    try:
        f = open(path, mode="w")
        f.close()
        f = open(path, mode="r")
        f.close()
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _test_imports() -> TestResult:
    try:
        import idna
        import idna.uts46data
        import urllib3
        from urllib3.contrib.hface.protocols._protocols import HTTP1Protocol
        import urllib3.contrib.hface.protocols.http1
        
        import rgbmatrix
        import rgbmatrix.core
        import rgbmatrix.graphics
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _hvv_generator() -> HVV:
    return HVV(DateHandler())

def _test_hvv() -> TestResult:
    hvv = _hvv_generator()
    try:
        hvv.set_bus_arrivals()
        # rsp = requests.post(url=hvv.GEOFOX_URL, headers=hvv.geofox_header, json=hvv.geofox_payload, timeout=20).json()
        # cv_rsp = hvv._convert_response(data=rsp)
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _test_fonts() -> TestResult:
    path = os.path.join(FONT_PATH, f"4x6.bdf")
    if os.path.exists(os.path.abspath(path)):
        filenames = os.listdir(FONT_PATH)
        
        if "4x6.bdf" in filenames:
            return TestResult(True, "Success!")
        else:
            return TestResult(False, f"Couldn't find the most commonly used font (Folder: {FONT_PATH}, File: {os.path.abspath(path)})")
    else:
        return TestResult(False, "Font path does not exist.")

def _test_matrix() -> TestResult:
    try:
        m = Matrix()
        m.process()
        m.draw_box(x1=1, y1=1, x2=16, y2=16, color=Color(255, 255, 255))
        m.matrix.SwapOnVSync(m.canvas)
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _test_weather_rsp() -> TestResult:
    try:
        w = WeatherAgent(DateHandler())
        w.weather
        w.current_temperature
        w.hour_index
        w.precipitation
        w.rain_forecast_avg
        w.precipitation_forecast(6)
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def test() -> None:
    print(_test_weather_cache().msg)
    print(_test_hvv().msg)
    print(_test_imports().msg)
    print(_test_fonts().msg)
    print(_test_weather_rsp().msg)
    print(_test_matrix().msg)

def pretty_tests() -> None:
    tests: List[Callable] = [
        _test_weather_cache,
        _test_hvv,
        _test_imports,
        _test_fonts,
        _test_weather_rsp,
        _test_matrix
    ]
    for test in tests:
        print(f"Running Test {Fore.LIGHTGREEN_EX}\"{test.__name__}\"{Fore.RESET}\t{test().msg}")

if __name__ == "__main__":
    test()