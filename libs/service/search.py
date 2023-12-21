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
        try:
            if self.__base_url not in pieces_url:
                return self.__base_url+pieces_url
            return pieces_url
        except Exception:
            return pieces_url


    def split_string(self, input_string: str, many: int):
        return [input_string[i:i+many] for i in range(0, len(input_string), many)]


    def news_release(self, url_artc: str) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        side_left = html.find('#srch > article > div > div > div:first-child > p')
        side_right = html.find('#srch > article > div > div > div:last-child')
        
        results = {
            "media_relations": {
                "contact1": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[0],
                "contact2": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[1],
                "email": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[2],
            },
            "spotlight": {
                "name": self.__parser.ex(html=side_right, selector="aside.researcher-spotlight > ul > li > div.researcher-titles > h3").text(),
                "profession": self.__parser.ex(html=side_right, selector="aside.researcher-spotlight > ul > li > div.researcher-titles > h4").text(),
                "biography": self.__parser.ex(html=side_right, selector="aside.researcher-spotlight > ul > li > p").text(),
                "profile_picture": {
                    "url_pict": self.__parser.ex(html=side_right, selector="#image-65562d69f8 > a > picture > img").attr("src"),
                    "width": self.__parser.ex(html=side_right, selector="#image-65562d69f8 > a > picture > img").attr("width"),
                    "height": self.__parser.ex(html=side_right, selector="#image-65562d69f8 > a > picture > img").attr("height"),
                    "desc": self.__parser.ex(html=side_right, selector="#image-65562d69f8 > a > picture > img").attr("alt"),
                },
            },
            "researcher": [{
                "research": self.__parser.ex(html=res, selector="a").text(),
                "profile": self.__parser.ex(html=res, selector="a").attr('href')
            }for res in self.__parser.ex(html=side_right, selector="aside:nth-child(3) > ul:nth-child(7) > li")],
            "topics": [{
              "url": self.__parser.ex(html=tag, selector="a").attr('href'),
              "tag": self.__parser.ex(html=tag, selector="a").text()
            }for tag in self.__parser.ex(html=side_right, selector="aside:nth-child(3) > ul:nth-child(5) > li")],
            "Article": self.__parser.ex(html=html, selector="#srch > article > div > div > div:first-child > p").text(),
        }

        return results


    def commentary(self, url_artc: str) -> dict:
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
                "tag": self.__parser.ex(html=tag, selector="a").text(),
            } for tag in self.__parser.ex(html=footer, selector="div.blog-column-right ul > li")],
            "Article": self.__parser.ex(html=footer, selector="div.body-text p").text()
        }

        return results
        

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
            }
        }

        match self.__parser.ex(html=pieces_table, selector='div.text p.type').text():
            case "Commentary":
                results.update({
                    "content": self.commentary(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                    })
                
            case "News Release":
                results.update({
                    "content": self.news_release(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                })

            case _:
                ic("hehe")


        return results

    def execute(self):
        response = requests.get(url="https://www.rand.org/news.html", headers=self.__headers)
        ic(response)
        html = PyQuery(response.text)
        table = html.find(selector='#results > ul')

        for line in table.find('li'):
            results = self.exstract_data(pieces_table=line)
            ic(results.get("title").replace(" ", "_"))
            self.__writer.ex(path=f'dumps/{results.get("title").replace(" ", "_").replace(":", "").replace("?", "")}.json', content=results)
            

