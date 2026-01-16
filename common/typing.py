from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta
)
from typing import (
    List,
    Tuple,
    Dict,
    Optional
)

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

Image = List[List[Pixel]]

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