import requests
from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic
from datetime import datetime as time
from libs.helpers.Parser import Parser
from libs.helpers.Writer import Writer
from libs.service.downloader import Downloader

class Research:
    def __init__(self) -> None:
        self.__parser = Parser()
        self.__writer = Writer()
        self.__download = Downloader()
        self.__results = {
            "categories": "research",
            "times": str(time.now()),
            "datas": []
        }

        self.__user_agent = FakeUserAgent()
        self.__headers = {
            'User-Agent': self.__user_agent.random
        }

    def exstract_article(self, url_artc: str) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        body = PyQuery(response.text)

        pass

    def exstract_data(self, pieces_table: str):
            
        results = {
            "type": self.__parser.ex(html=pieces_table, selector='div.text p.type').text(),
            "title": self.__parser.ex(html=pieces_table, selector='div.text h3.title').text(),
            "url": self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'),
            "descriptions": self.__parser.ex(html=pieces_table, selector='div.text p.desc').text(),
            "posted": self.__parser.ex(html=pieces_table, selector='div.text p.date').text(),
            "image": {
                "thumb": self.__parser.ex(html=pieces_table, selector='div.img-wrap a img').attr('src'),
                "desc": self.__parser.ex(html=pieces_table, selector='div.img-wrap a img').attr('alt'),
            }
        }

        self.__writer.ex(path='private/news.json', content=self.__results)

        return results

    def execute(self):
        response = requests.get(url="https://www.rand.org/news.html", headers=self.__headers)

        html = PyQuery(response.text)
        table = html.find(selector='#results > ul')

        for line in table.find('li'):
            results = self.exstract_data(pieces_table=line)
