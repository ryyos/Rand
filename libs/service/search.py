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
        self.__base_url = 'https://www.rand.org'
        self.__user_agent = FakeUserAgent()
        self.__headers = {
            'User-Agent': self.__user_agent.random
        }


    def complement_url(self, pieces_url: str) -> str:
        if self.__base_url not in pieces_url:
            return self.__base_url+pieces_url
        return pieces_url


    def exstract_article(self, url_artc: str) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        header = html.find('#srch > article > div.post-heading')
        footer = html.find('#srch > article > div.constrain-width')
        
        results = {
            "source": self.__parser.ex(html=header, selector="p.source").text(),
            "author": {
                "name": self.__parser.ex(html=footer, selector="p.authors > a").text(),
                "profil": self.complement_url(self.__parser.ex(html=footer, selector="p.authors > a").attr('href')),
                "position": self.__parser.ex(html=footer, selector="div.blog-column-left h4").text(),
                "username": self.__parser.ex(html=footer, selector="div.blog-column-left p > a").text(),
                "contact": self.__parser.ex(html=footer, selector="div.blog-column-left p > a").attr('href')
            },
            "topic": [{
                "blog": self.complement_url(self.__parser.ex(html=tag, selector="a").attr('href')),
                "tags": self.__parser.ex(html=tag, selector="a").text(),
            } for tag in self.__parser.ex(html=footer, selector="div.blog-column-right ul > li")],
            "Article": self.__parser.ex(html=footer, selector="div.body-text p").text()
        }

        self.__writer.ex(path='private/artc.json', content=results)
        ic(results)
        

    def exstract_data(self, pieces_table: str):
            
        results = {
            "type": self.__parser.ex(html=pieces_table, selector='div.text p.type').text(),
            "title": self.__parser.ex(html=pieces_table, selector='div.text h3.title').text(),
            "url": self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'),
            "descriptions": self.__parser.ex(html=pieces_table, selector='div.text p.desc').text(),
            "posted": self.__parser.ex(html=pieces_table, selector='div.text p.date').text(),
            "image": {
                "thumb": self.complement_url(self.__parser.ex(html=pieces_table, selector='div.img-wrap a img').attr('src')),
                "desc": self.__parser.ex(html=pieces_table, selector='div.img-wrap a img').attr('alt'),
            },
            "content": self.exstract_article(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
        }

        self.__writer.ex(path='private/results.json', content=results)

        return results

    def execute(self):
        response = requests.get(url="https://www.rand.org/news.html", headers=self.__headers)

        html = PyQuery(response.text)
        table = html.find(selector='#results > ul')

        for line in table.find('li'):
            results = self.exstract_data(pieces_table=line)
