from libs import Research
from libs import Downloader

if __name__ == '__main__':
    search = Research()
    search.exstract_url(page_url='kk')

    # download = Downloader()
    # download.download(url="https://www.rand.org/content/dam/rand/pubs/testimonies/CTA3000/CTA3097-1/RAND_CTA3097-1.pdf")
