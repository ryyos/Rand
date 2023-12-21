import requests
from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic

from libs.helpers.Parser import Parser
from libs.helpers.Writer import Writer

class Research:
    def __init__(self) -> None:
        self.__user_agent = FakeUserAgent()
        self.__parser = Parser()
        self.__writer = Writer()
        self.__headers = {
            'User-Agent': self.__user_agent.random
        }


    def filter_data(self, page_url: str):
        response = requests.get(url="https://www.rand.org/pubs.html?page=5", headers=self.__headers)
        ic(response)
        html = PyQuery(response.text)
        body = html.find(selector='#results ul')
        self.__writer.exstr(path='private/body.html', content=str(body))

    def execute(self):
        response = requests.get(url='')

