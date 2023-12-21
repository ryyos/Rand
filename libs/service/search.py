import requests
from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic

from datetime import datetime
from time import time
from libs.helpers.Parser import Parser
from libs.helpers.Writer import Writer
from libs.service.downloader import Downloader

class Search:
    def __init__(self) -> None:
        self.__parser = Parser()
        self.__writer = Writer()
        self.__download = Downloader()
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


    def media_advisory(self, url_artc: str) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        side_right = html.find('#srch > article > div > div > div:last-child')
        
        results = {
            "media_relations": {
                "contact1": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[0].replace("\n", ""),
                "contact2": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[1].replace("\n", ""),
                "email": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[2],
            },
            "sub_content": [{
                self.__parser.ex(html=sub, selector="h2").text(): self.__parser.ex(html=sub, selector="p").text()
            }for sub in self.__parser.ex(html=html, selector="#srch > article > div > div > div.eight.columns div")],
            "topics": [{
              "url": self.complement_url(self.__parser.ex(html=tag, selector="a").attr('href')),
              "tag": self.__parser.ex(html=tag, selector="a").text()
            }for tag in self.__parser.ex(html=side_right, selector="aside:last-child > ul > li")],
            "Article": self.__parser.ex(html=html, selector="#srch > article > div > div > div:first-child > p").text(),
        }

        return results


    def essay(self, url_artc) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        body = html.find(selector="#srch > article")
        side = html.find(selector="#srch > article > div.constrain-width > div.blog-column-right")

        results = {
            "article": self.__parser.ex(html=body, selector="div.body-text p").text(),
            "overview": self.__parser.ex(html=body, selector="div.overview > p").text(),
            "topine": self.__parser.ex(html=body, selector="div.topline > div > ul > li").text(),
            "topics": [
                {
                    "tag": self.__parser.ex(html=tag, selector="a").text(),
                    "blog": self.complement_url(self.__parser.ex(html=tag, selector="a").attr('href')),
                } for tag in side.find(selector="aside.related-topics > ul > li")
            ],
            "image": [
                {
                    "url_image": self.complement_url(pieces_url=self.__parser.ex(html=img, selector="img").attr("src")),
                    "width": self.__parser.ex(html=img, selector="img").attr("width"),
                    "height": self.__parser.ex(html=img, selector="img").attr("height"),
                    "desc": self.__parser.ex(html=img, selector="img").attr("alt"),
                }for img in body.find(selector='div.body-text div[data-cmp-hook-image="imageV3"] > picture')
            ]
        }


    def article(self, url_artc) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        body = html.find(selector="#srch > article > div.body-wrap")
        side = html.find(selector="#srch > article > div.body-wrap > div.digital-article-right")

        results = {
            "article": self.__parser.ex(html=body, selector="div.body-text p").text(),
            "overview": self.__parser.ex(html=body, selector="div.overview > p").text(),
            "topine": self.__parser.ex(html=body, selector="div.topline > div > ul > li").text(),
            "topics": [
                {
                    "tag": self.__parser.ex(html=tag, selector="a").text(),
                    "blog": self.complement_url(self.__parser.ex(html=tag, selector="a").attr('href')),
                } for tag in side.find(selector="aside.related-topics > ul > li")
            ],
            "image": [
                {
                    "url_image": self.complement_url(pieces_url=self.__parser.ex(html=img, selector="img").attr("src")),
                    "width": self.__parser.ex(html=img, selector="img").attr("width"),
                    "height": self.__parser.ex(html=img, selector="img").attr("height"),
                    "desc": self.__parser.ex(html=img, selector="img").attr("alt"),
                }for img in body.find(selector='div.body-text div[data-cmp-hook-image="imageV3"] > picture')
            ]
        }

        return results

    def blog(self, url_artc: str) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        body = html.find(selector="#srch > article > div.constrain-width")
        side = html.find(selector="#srch > article > div.constrain-width > div.blog-column-right")

        results = {
            "topic": [{
                "tag": self.__parser.ex(html=tag, selector="a").text(),
                "blog": self.complement_url(self.__parser.ex(html=tag, selector="a").attr("href"))
            }for tag in self.__parser.ex(html=side, selector="aside.related-topics > ul > li")],
            "Article": self.__parser.ex(html=body, selector="div.body-text > p").text(),
            "sub_article": [
                {
                    "title": self.__parser.ex(html=one, selector="h2.recap-heading").text(),
                    "descriptions": PyQuery(self.__parser.ex(html=one, selector="p")[1:]).text(),
                    "image": {
                        "url_image": self.complement_url(pieces_url=self.__parser.ex(html=one, selector="div:first-child > a > picture > img").attr("src")),
                        "width": self.__parser.ex(html=one, selector="div:first-child > a > picture > img").attr("width"),
                        "height": self.__parser.ex(html=one, selector="div:first-child > a > picture > img").attr("height"),
                        "desc": self.__parser.ex(html=one, selector="div:first-child > a > picture > img").attr("alt"),
                    }
                } for one in self.__parser.ex(html= body, selector="div.body-text > div.recap")
            ]
            
            
        }

        return results


    def announcement(self, url_artc: str) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        side_right = html.find(selector="#rightcolumn > aside")

        results = {
            "spotlight": {
                "quoted": self.__parser.ex(html=side_right, selector="ul > li > div > p").text(),
                "name": self.__parser.ex(html=side_right, selector="ul > li > div > div.text > h3 > a").text(),
                "profile": self.__parser.ex(html=side_right, selector="ul > li > div > div.text > h3 > a").attr("href"),
                "profession": self.__parser.ex(html=side_right, selector="ul > li > div > div.text > h4").text(),
                "profile_picture": {
                    "url_pict": self.complement_url(self.__parser.ex(html=side_right, selector="ul > li > div > div > a > picture > img").attr('src')),
                    "width": self.__parser.ex(html=side_right, selector="ul > li > div > div > a > picture > img").attr('width'),
                    "height": self.__parser.ex(html=side_right, selector="ul > li > div > div > a > picture > img").attr('height'),
                    "desc": self.__parser.ex(html=side_right, selector="ul > li > div > div > a > picture > img").attr('alt'),
                },
                "Article": self.__parser.ex(html=html, selector="#srch p").text()
            }
        }

        return results


    def news_release(self, url_artc: str) -> dict:
        response = requests.get(url=url_artc, headers=self.__headers)
        html = PyQuery(response.text)

        side_right = html.find('#srch > article > div > div > div:last-child')
        
        results = {
            "media_relations": {
                "contact1": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[0].replace("\n", ""),
                "contact2": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[1].replace("\n", ""),
                "email": self.split_string(self.__parser.ex(html=side_right, selector="aside.media-contact > p").text(), 15)[2],
            },
            "spotlight": {
                "name": self.__parser.ex(html=side_right, selector="aside.researcher-spotlight > ul > li > div.researcher-titles > h3").text(),
                "profession": self.__parser.ex(html=side_right, selector="aside.researcher-spotlight > ul > li > div.researcher-titles > h4").text(),
                "biography": self.__parser.ex(html=side_right, selector="aside.researcher-spotlight > ul > li > p").text(),
                "profile_picture": {
                    "url_pict": self.complement_url(self.__parser.ex(html=side_right, selector="div.bio.image > div > a > picture > img").attr("src")),
                    "width": self.__parser.ex(html=side_right, selector="div.bio.image > div > a > picture > img").attr("width"),
                    "height": self.__parser.ex(html=side_right, selector="div.bio.image > div > a > picture > img").attr("height"),
                    "desc": self.__parser.ex(html=side_right, selector="div.bio.image > div > a > picture > img").attr("alt"),
                },
            },
            "researcher": [{
                "research": self.__parser.ex(html=res, selector="a").text(),
                "profile": self.complement_url(self.__parser.ex(html=res, selector="a").attr('href'))
            }for res in self.__parser.ex(html=side_right, selector="aside:nth-child(3) > ul:nth-child(7) > li")],
            "topics": [{
              "url": self.complement_url(self.__parser.ex(html=tag, selector="a").attr('href')),
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
            "domain": "www.rand.org",
            "crawling_time": str(datetime.now()),
            "crawling_time_epoch": int(time()),
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

        ic(self.__parser.ex(html=pieces_table, selector='div.text h3.title').text())
        match self.__parser.ex(html=pieces_table, selector='div.text p.type').text():
            case "Commentary":
                results.update({
                    "content": self.commentary(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                    })
                
            case "News Release":
                results.update({
                    "content": self.news_release(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                })

            case "Announcement":
                results.update({
                    "content": self.announcement(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                })

            case "Blog":
                results.update({
                    "content": self.blog(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                })

            case "ARTICLE":
                results.update({
                    "content": self.article(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                })

            case "ESSAY":
                results.update({
                    "content": self.essay(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                })

            case "MEDIA ADVISORY":
                results.update({
                    "content": self.media_advisory(url_artc=self.__parser.ex(html=pieces_table, selector='div.text h3.title a').attr('href'))
                })

            case _:
                ic("belum ada")
                ic(self.__parser.ex(html=pieces_table, selector='div.text p.type').text())
                ic(self.__parser.ex(html=pieces_table, selector='div.text h3.title').text())


        return results

    def execute(self, url: str):
        response = requests.get(url=url, headers=self.__headers)
        ic(response)
        html = PyQuery(response.text)
        table = html.find(selector='#results > ul')

        if len(table) == 0: return "clear"

        for line in table.find('li'):
            results = self.exstract_data(pieces_table=line)
            self.__writer.ex(path=f'data/{results.get("title").replace(" ", "_").replace(":", "").replace("?", "")}.json', content=results)
            return "extant"
            

