import requests
from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic
from datetime import datetime as time
from libs.helpers.Parser import Parser
from libs.helpers.Writer import Writer

class Research:
    def __init__(self) -> None:
        self.__user_agent = FakeUserAgent()
        self.__parser = Parser()
        self.__writer = Writer()
        self.__results = {
            "categories": "research",
            "times": str(time.now()),
            "datas": []
        }
        self.__headers = {
            'User-Agent': self.__user_agent.random
        }


    def exstract_url(self, page_url: str):
        urls = []
        response = requests.get(url="https://www.rand.org/pubs.html?page=5", headers=self.__headers)
        ic(response)
        html = PyQuery(response.text)
        table = html.find(selector='#results > ul')

        for line in table.find('li'):
            
            results = {
                "type": self.__parser.ex(html=line, selector='div.text p.type').text(),
                "title": self.__parser.ex(html=line, selector='div.text h3.title').text(),
                "url": self.__parser.ex(html=line, selector='div.text h3.title a').attr('href'),
                "descriptions": self.__parser.ex(html=line, selector='div.text p.desc').text(),
                "posted": self.__parser.ex(html=line, selector='div.text p.date').text(),
                "authors": self.__parser.ex(html=line, selector='div.text p.authors').text(),
                "image": {
                    "thumb": self.__parser.ex(html=line, selector='div.img-wrap a img').attr('src'),
                    "desc": self.__parser.ex(html=line, selector='div.img-wrap a img').attr('alt'),
                }
            }

            self.__results['datas'].append(results)
        
            urls.append(results.get('url'))
        # self.__writer.ex(path='private/result1.json', content=self.__results)


    def execute(self):
        response = requests.get(url='')

