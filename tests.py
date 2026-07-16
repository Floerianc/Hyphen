import platform
import traceback
import pkg_resources
import os

from core import proxy

os.chdir(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)

from dataclasses import dataclass
from dotenv import load_dotenv
from colorama import Fore
from typing import (
    Callable,
    List
)

import core.dawum as dawum
from core.hvv import HVV
from core.weather import WeatherAgent
from core.dates import DateHandler
from core.holidays import Holidays
from core.canvas import Matrix
from common.typing import Color
from util.utils import FONT_PATH

load_dotenv()

@dataclass
class TestResult:
    success: bool
    msg: str

def _test_weather_cache() -> TestResult:
    """Checks if the program is able to read and write
    into the weather cache.

    Returns:
        TestResult: Successful or not :)
    """
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
    """Tests critical imports that have caused
    problems in the past.

    If idna or urllib misses: Just install the packages
    
    If idna.uts46data or the other urllib packages are missing:
    try reinstalling or updating them.
    
    If rgbmatrix is missing: you're cooked, try recompiling it

    Returns:
        TestResult: Successful or not
    """
    try:
        import idna
        import idna.uts46data
        import urllib3
        from urllib3.contrib.hface.protocols._protocols import HTTP1Protocol
        import urllib3.contrib.hface.protocols.http1
        
        import rgbmatrix
        import rgbmatrix.core       # type: ignore
        import rgbmatrix.graphics   # type: ignore
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _hvv_generator() -> HVV:
    """Creates a valid HVV controller

    Returns:
        HVV: HVV class
    """
    return HVV(DateHandler())

def _test_hvv() -> TestResult:
    """Tests if the API response from HVV is valid
    and available

    Returns:
        TestResult: Successful or not
    """
    hvv = _hvv_generator()
    try:
        hvv.set_bus_arrivals()
        # rsp = requests.post(url=hvv.GEOFOX_URL, headers=hvv.geofox_header, json=hvv.geofox_payload, timeout=20).json()
        # cv_rsp = hvv._convert_response(data=rsp)
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _test_fonts() -> TestResult:
    """Tests if program can access fonts 

    Returns:
        TestResult: Successful or not
    """
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
    """Tests a few core functionalities in the Matrix
    class to check if it is possible to communicate
    with the LED Panel

    Returns:
        TestResult: Successful or not
    """
    try:
        m = Matrix()
        m.process()
        m.draw_box(x1=1, y1=1, x2=16, y2=16, color=Color(255, 255, 255))
        m.matrix.SwapOnVSync(m.canvas)
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _test_weather_rsp() -> TestResult:
    """Tests if the weather API is working accordingly

    Returns:
        TestResult: Successful or not
    """
    try:
        w = WeatherAgent(DateHandler())
        # w.weather
        w.hourly_variable_len
        w.current_temperature
        w.hour_index
        w.precipitation
        w.rain_forecast_avg
        w.precipitation_forecast(6)
        w._fetch_weather()
        return TestResult(True, "Success!")
    except Exception as e:
        return TestResult(False, str(e))

def _test_dawum() -> TestResult:
    try:
        if os.environ.get("DAWUM_URL", ""):
            d = dawum.DAWUM()
            d.update()
            return TestResult(True, "Success!")
        else:
            return TestResult(False, "URL can not be found in os.environ")
    except Exception as e:
        return TestResult(False, str(e))

def _test_proxy() -> TestResult:
    try:
        session = proxy.SessionWrapper(timeout=20)
        request = proxy.RequestWrapper(timeout=20)
        rsp = request.request("GET", "https://example.com/", {})
        rsp2 = session.request("GET", "https://example.com", {})
        if rsp and rsp2:
            return TestResult(True, "Success!")
        else:
            return TestResult(False, f"Invalid responses; 1: {rsp.text}\t2: {rsp.text}")
    except Exception as e:
        return TestResult(False, str(e))

def _test_perms() -> TestResult:
    """Checks if the program is run with admin rights
    
    This is important because the rgbmatrix module
    needs admin rights to set the maximum priority
    of the program so there isn't much flickering
    on the panel.

    Returns:
        TestResult: Is running with admin or not
    """
    if platform.system() == "Windows":
        try:
            temp = os.listdir(os.sep.join([os.environ.get("SystemRoot", "C:\\windows"), "temp"]))
        except Exception as e:
            return TestResult(False, str(e))
        else:
            return TestResult(True, "Success!")
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return TestResult(True, "Success!")
        else:
            return TestResult(False, "Not using sudo.")

def _test_packages() -> TestResult:
    """Checks if the correct packages are installed

    This is really important because some
    packages are colliding with each other if you
    have the wrong version installed
    
    the requirements.txt shipped with the program
    should install every needed package

    Returns:
        TestResult: Returns missing and mismatching packages if necessary
    """
    installed_packages = pkg_resources.working_set.by_key
    requirements: List[str] = open("./requirements.txt", "r", encoding="UTF-8").readlines()
    missing = []
    mismatches = []
    
    packages = list(installed_packages.keys())
    distributions = list(installed_packages.values())
    for requirement in requirements:
        package, version = requirement.split("==")
        version = version.removesuffix("\n")
        if package in packages:
            idx = packages.index(package)
            dist = distributions[idx]
            if dist.version == version:
                continue
            else:
                mismatches.append([(packages[idx], distributions[idx].version), (package, version)])
        else:
            missing.append((package, version))
    
    if not missing and not mismatches:
        return TestResult(True, "Success!")
    else:
        return TestResult(False, f"Missing:\t{missing},\n\t\t\t\tMismatches: {mismatches}")

def _test_holidays() -> TestResult:
    try:
        h = Holidays(DateHandler())
        h.update()
        h.next_n_holidays(2)
        return TestResult(True, f"Success!")
    except Exception as e:
        return TestResult(False, str(e))

def pretty_tests() -> None:
    tests: List[Callable] = [
        _test_weather_cache,
        _test_hvv,
        _test_holidays,
        _test_imports,
        _test_fonts,
        _test_weather_rsp,
        _test_matrix,
        _test_perms,
        _test_packages,
        _test_dawum,
        _test_proxy
    ]
    for test in tests:
        print(f"Running Test {Fore.LIGHTGREEN_EX}\"{test.__name__}\"{Fore.RESET}\t{test().msg}")

if __name__ == "__main__":
    # test
    # pretty_tests()
    print(dawum.DAWUM().format_survey(dawum.DAWUM().get_latest_survey()))