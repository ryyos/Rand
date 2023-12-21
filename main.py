from libs import Research
from libs import Downloader

if __name__ == '__main__':
    search = Research()
    # search.exstract_article(url_artc='https://www.rand.org/pubs/commentary/2023/12/vietnams-show-of-welcome-for-xi-reflects-growing-self.html')
    search.execute()
    # search.news_release("https://www.rand.org/news/press/2023/12/04.html")

    # download = Downloader()
    # download.download(url="https://www.rand.org/content/dam/rand/pubs/testimonies/CTA3000/CTA3097-1/RAND_CTA3097-1.pdf")
