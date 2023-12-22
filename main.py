from libs import Search
from libs import Downloader
from icecream import ic

class Main:
    def __init__(self) -> None:
        self.__search = Search()
        self.__base_url = "https://www.rand.org/news.html"

    def main(self):
        page = 1

        while True:
            ic(page)
            conditions = self.__search.execute(url=f"{self.__base_url}?page={page}")
            if conditions: break
            page += 1



if __name__ == '__main__':
    search = Main()
    search.main()

    
