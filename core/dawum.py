import os
import dacite
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from typing import (
    Dict,
    List,
    Union,
    Optional
)
from common.logger import log_event
from common.typing import Color
from core.proxy import SessionWrapper

load_dotenv()

DAWUM_URL = os.environ.get("DAWUM_URL", "")

@dataclass
class Survey:
    Date: datetime
    Survey_Period: Dict[str, datetime]
    Surveyed_Persons: int
    Parliament: str
    Institute: str
    Tasker: str
    Method: str
    Results: Dict[str, Union[int, float]]
    
    @classmethod
    def _from_dict(
        cls,
        data: dict
    ) -> 'Survey':
        return dacite.from_dict(Survey, data=data)


class DAWUM:
    def __init__(self) -> None:
        self.session = SessionWrapper(timeout=20)
        self.latest_survey: Optional[Survey]
        
        rsp = self.session.request("GET", url=DAWUM_URL).json()  # <-- Only needed to store the conversions
        del rsp["Surveys"]
        self.PARLIAMENTS: Dict[str, Dict[str, str]] = rsp["Parliaments"]
        self.INSTITUTES: Dict[str, Dict[str, str]] = rsp["Institutes"]
        self.TASKERS: Dict[str, Dict[str, str]] = rsp["Taskers"]
        self.METHODS: Dict[str, Dict[str, str]] = rsp["Methods"]
        self.PARTIES: Dict[str, Dict[str, str]] = rsp["Parties"]
        self.PARTY_COLORS = {
            "AfD": "#0489DB",
            "Bayernpartei": "#0080FF",
            "BVB/FW": "#FFA500",
            "Grüne": "#1AA037",
            "BD": "#FFEF00",
            "BSW": "#7A1B51",
            "bunt.saar": "#F17720",
            "BfTh": "#005999",
            "CDU/CSU": "#2d3c4b",
            "CDU": "#003B6F",
            "CSU": "#0570C9",
            "Linke": "#bd3075",
            "Familie": "#FF6600",
            "FDP": "#FFEF00",
            "Freie Wähler": "#063E8F",
            "NPD": "#EB0019",
            "ÖDP": "#EE7100",
            "Die PARTEI": "#B92837",
            "Tierschutzpartei": "#C722B3",
            "Piraten": "#FE7400",
            "Plus Brandenburg": "#782E8F",
            "SPD": "#E3000F",
            "SSW": "#00277E",
            "Volt": "#a134c9",
            "WerteUnion": "#013B5B",
            "Sonstige": "#787878",
        }
        
        self.update()

    def _only_relevant(self, results: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        copy = results.copy()
        for party, result in copy.items():
            if result < 5.0 and party != "0":
                results.__delitem__(party)
        del copy
        return results

    def get_latest_survey(
        self,
        parliament: str = "0"
    ) -> Optional[Survey]:
        rsp = self.session.request(
            "GET",
            url=DAWUM_URL
        )
        if not rsp.ok:
            log_event(f"Could not get survey results from \"{DAWUM_URL}\"", "ERROR")
            return None
        else:
            surveys = rsp.json()["Surveys"]
            for _, survey in surveys.items():
                if survey["Parliament_ID"] == parliament:
                    return self._convert_response(survey)
            return None

    def _convert_response(self, data: dict) -> Survey:
        relevant_results = self._only_relevant(data["Results"])
        results = {self.PARTIES.get(party, {})["Shortcut"]: value for party, value in relevant_results.items()}
        results["Sonstige"] = results.pop("Sonstige")
        
        return Survey(
            Date=datetime.strptime(data["Date"], "%Y-%m-%d"),
            Survey_Period={key: datetime.strptime(date, "%Y-%m-%d") for key, date in data["Survey_Period"].items()},
            Surveyed_Persons=int(data["Surveyed_Persons"]),
            Parliament=self.PARLIAMENTS.get(data["Parliament_ID"], {"Name": ""})["Name"],
            Institute=self.INSTITUTES.get(data["Institute_ID"], {"Name": ""})["Name"],
            Tasker=self.TASKERS.get(data["Tasker_ID"], {"Name": ""})["Name"],
            Method=self.METHODS.get(data["Method_ID"], {"Name": ""})["Name"],
            Results=results
        )
    
    def update(self) -> None:
        newest = self.get_latest_survey()
        if newest:
            self.latest_survey = newest
    
    def get_colors(
        self,
        survey: Survey
    ) -> List[Color]:
        return [Color.from_hex(self.PARTY_COLORS.get(party, "#000000")) for party in survey.Results.keys()]