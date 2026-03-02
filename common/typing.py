import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta
)
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Tuple,
    Optional,
    Union
)
from threading import Thread
from common.logger import log_event


@dataclass
class Color:
    """A helper class to define colors instead of
    using a tuple
    """
    r: int
    g: int
    b: int
    
    def __post_init__(self) -> None:
        assert self.r < 256 and self.r >= 0
        assert self.g < 256 and self.g >= 0
        assert self.b < 256 and self.b >= 0
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @rgb.setter
    def rgb(
        self,
        value: Tuple[int, int, int]
    ) -> None:
        self.r, self.g, self.b = value

@dataclass
class Pixel:
    """A dataclass for a single pixel on the LED panel
    """
    on: bool
    color: Optional[Color] = None


@dataclass
class BusArrival:
    """Dataclass to show the necessary for when a specific
    bus arrives at a certain destination
    """
    line: int
    destination: str
    time: datetime
    delay: timedelta


@dataclass
class GeoFoxTime:
    """Dataclass for the time object the GeoFox API returns
    """
    date: str # '23.12.2025'
    time: str # '05:39'


@dataclass
class GeoFoxDepartureStation:
    """Dataclass for the departure station object from the GeoFox API
    
    id and globalId contains information to identify the station
    in HVV's internal database or something 
    """
    combinedName: str
    id: str
    globalId: str


@dataclass
class GeoFoxDepartureLineType:
    """Dataclass containing information about a certain bus that
    arrives at the destination
    """
    simpleType: str
    shortInfo: str
    longInfo: str
    model: str


@dataclass
class GeoFoxDepartureLine:
    """Dataclass containing information about the line

    * name = the number code of the line (e.g. 218)
    * direction = the last station the bus stops at
    * origin = where the bus line starts
    * type = information about the arriving bus
    * id = internal information about the line
    * dlid = internal information about the line
    """
    name: str
    direction: str
    origin: str
    type: GeoFoxDepartureLineType
    id: str
    dlid: str


@dataclass
class GeoFoxDeparture:
    """Dataclass with additional information about the departure of a bus

    * line: Information about the line of the bus
    * directionId: 1 -> forward; 6 -> backward
    * timeOffset: In how many minutes the bus will arrive
    * delay: Delay of bus in seconds
    * serviceId: ID of the bus line/route
    * station: Information about the station the bus arrives on
    """
    line: GeoFoxDepartureLine
    directionId: int
    timeOffset: int
    delay: int
    serviceId: int
    station: GeoFoxDepartureStation


@dataclass
class GeoFoxResponse:
    """Dataclass to help use the JSON Response from the
    GeoFox API
    """
    returnCode: str
    time: GeoFoxTime
    departures: List[GeoFoxDeparture]


# Unused for now
class StopableThread(Thread):
    def __init__(
        self,
        interval: Union[float, int],
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None, args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None,
    ) -> None:    # type: ignore
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.stop: bool = False
        self.target = target
        self.args = args
        self.interval = interval
    
    @property
    def stopped(self) -> bool:
        return self.stop
    
    def set_stopped(self, boolean: bool) -> None:
        self.stop = boolean
    
    def run(self) -> None:
        next_time = time.time() + self.interval
        while True and not self.stopped and self.target:
            time.sleep(max(0, next_time - time.time()))
            try:
                self.target(*self.args)
            except Exception:
                log_event("Error while executing repetitive method.", "ERROR")
            next_time += (time.time() - next_time) // self.interval * self.interval + self.interval
        else:
            ...


Image = List[List[Pixel]]

@dataclass
class PollenSeverity:
    description: str
    color: Color


SeverityMap = Dict[str, PollenSeverity]


@dataclass
class Box:
    x1: int
    x2: int
    y1: int
    y2: int