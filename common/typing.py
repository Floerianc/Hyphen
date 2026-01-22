from collections.abc import Callable
from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta
)
from typing import (
    Any,
    Iterable,
    List,
    Mapping,
    Tuple,
    Optional
)
from threading import Thread

@dataclass
class Color:
    """A helper class to define colors instead of
    using a tuple
    """
    r: int
    g: int
    b: int
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @rgb.setter
    def rgb(self, value: Tuple[int, int, int]) -> None:
        self.r, self.g, self.b = value

@dataclass
class Pixel:
    on: bool
    color: Optional[Color] = None


@dataclass
class BusArrival:
    line: int
    destination: str
    time: datetime
    delay: timedelta


@dataclass
class GeoFoxTime:
    date: str # '23.12.2025'
    time: str # '05:39'


@dataclass
class GeoFoxDepartureStation:
    combinedName: str
    id: str
    globalId: str


@dataclass
class GeoFoxDepartureLineType:
    simpleType: str
    shortInfo: str
    longInfo: str
    model: str


@dataclass
class GeoFoxDepartureLine:
    name: str
    direction: str
    origin: str
    type: GeoFoxDepartureLineType
    id: str
    dlid: str


@dataclass
class GeoFoxDeparture:
    line: GeoFoxDepartureLine
    directionId: int
    timeOffset: int
    delay: int
    serviceId: int
    station: GeoFoxDepartureStation


@dataclass
class GeoFoxResponse:
    returnCode: str
    time: GeoFoxTime
    departures: List[GeoFoxDeparture]


# Unused for now
class StopableThread(Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.stop: bool = False
        self.target = target
        self.args = args
    
    @property
    def stopped(self) -> bool:
        return self.stop
    
    def set_stopped(self, boolean: bool) -> None:
        self.stop = boolean
    
    def run(self) -> None:
        while True and not self.stopped and self.target:
            self.target(*self.args)

Image = List[List[Pixel]]