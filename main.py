from libs import Search
from libs import Downloader

# class Main:
#     def __init__(self) -> None:
#         self.__search = Search()
#         self.__base_url = "https://www.rand.org/news.html"

#     def main(self):
#         page = 1

#         while True:
#             conditions = self.__search.execute(url=f"{self.__base_url}?page={page}")
#             if conditions == "clear": break
#             page += 1



# if __name__ == '__main__':
#     search = Main()
#     search.main()

if __name__ == '__main__':
    search = Search()
    # search.blog("https://www.rand.org/pubs/articles/2023/weekly-recap-november-03.html")
    search.article("https://www.rand.org/pubs/articles/2022/synthetic-opioids-are-an-everything-problem.html")
    
