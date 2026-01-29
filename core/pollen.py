import requests
from typing import (
    Dict,
    List
)
from common.typing import (
    Color,
    PollenSeverity,
    SeverityMap
)

class DWDPollen:
    def __init__(self) -> None:
        self.region_ID = 10
        self.URL = "https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json"
        self.data: dict = requests.get(self.URL).json()
        self.sev_map: SeverityMap = {
            '0':    PollenSeverity('keine Belastung', Color(0, 255, 0)),
            '0-1':  PollenSeverity('keine bis geringe Belastung', Color(43, 212, 0)),
            '1':    PollenSeverity('geringe Belastung', Color(86, 169, 0)),
            '1-2':  PollenSeverity('geringe bis mittlere Belastung', Color(129, 126, 0)),
            '2':    PollenSeverity('mittlere Belastung', Color(173, 83, 0)),
            '2-3':  PollenSeverity('mittlere bis hohe Belastung', Color(216, 40, 0)),
            '3':    PollenSeverity('hohe Belastung', Color(255, 0, 0)),
            'NDF':  PollenSeverity('Keine Daten', Color(255, 0, 255))
        }
    
    def update(self) -> None:
        new_data: dict = requests.get(self.URL).json()
        if new_data:
            self.data = new_data
    
    def get_region(self) -> dict:
        for l in self.data['content']:
            if l['region_id'] == self.region_ID:
                return l
        return {}
    
    def get_pollen(self) -> dict:
        return self.get_region()['Pollen']
    
    def get_pollen_severity(
        self,
        pollen: List[str]
    ) -> Dict[str, PollenSeverity]:
        data = self.get_pollen()
        return {
            pollen_name: self.sev_map[data[pollen_name]['today']] for pollen_name in pollen
        }