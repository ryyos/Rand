import requests

from fake_useragent import FakeUserAgent
from libs.helpers.Writer import Writer

class Downloader:
    def __init__(self) -> None:
        self.__user_agent = FakeUserAgent()
        self.__writer = Writer()
        self.__headers = {
            'User-Agent': self.__user_agent.random
        }

    def ex(self, url: str, path: str):
        response = requests.get(url=url, headers=self.__headers)
        print(response)
        self.__writer.eby(path=path, media=response)