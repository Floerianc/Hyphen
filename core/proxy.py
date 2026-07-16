# IMPORTANT NOTE! -- The proxy function is not yet implemented but will soon be added as I already found a work-around for my problem

import time
import requests
from fake_useragent import UserAgent
from typing import (
    Dict,
    Optional,
    Literal
)
from common.logger import log_event

Method = Literal["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

class RequestWrapper:
    def __init__(
        self,
        timeout=None
    ) -> None:
        self.timeout = timeout
        self.ua = UserAgent(browsers=["Chrome", "Firefox", "Edge"])
    
    @property
    def user_agent(self) -> str:
        return self.ua.random
    
    @property
    def header(self) -> Dict[str, str]:
        return {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
        }
    
    @property
    def proxy(self) -> ...:
        ...
    
    def request(
        self,
        method: Method,
        url: str,
        json: Optional[Dict] = None
    ) -> requests.Response:
        retries = 0
        factor = 2
        recent: requests.Response = None
        
        while True:
            try:
                recent = requests.request(
                    method=method,
                    url=url,
                    json=json,
                    headers=self.header
                )
                assert recent.ok == True # Honestly idk if it's better to use .ok or .status_code == 200
                return recent
            except:
                if retries > 5:
                    log_event(f"Couldn't get a server response from: \"{url}\"\tError code: {recent.status_code if recent else 'Unknown'}", "WARNING")
                    return recent
                time.sleep(factor**retries)
                retries += 1


class SessionWrapper(RequestWrapper):
    def __init__(self, timeout=None) -> None:
        super().__init__(timeout)
        self.session = requests.Session()
    
    def request(
        self,
        method: Method,
        url: str,
        json: Optional[Dict] = None
    ) -> requests.Response:
        retries = 0
        factor = 2
        recent: requests.Response = None
        
        while True:
            try:
                recent = self.session.request(
                    method=method,
                    url=url,
                    json=json,
                    headers=self.header
                )
                assert recent.ok == True # Honestly idk if it's better to use .ok or .status_code == 200
                return recent
            except:
                if retries > 5:
                    log_event(f"Couldn't get a server response from: \"{url}\"\tError code: {recent.status_code if recent else 'Unknown'}", "WARNING")
                    return recent
                time.sleep(factor**retries)
                retries += 1