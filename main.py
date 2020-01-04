import urllib
import urllib.request
from bs4 import BeautifulSoup
import os
from string import ascii_lowercase
from pathlib import Path

from urllib.request import Request, urlopen

base_url = "https://www.mangareader.net"
savelocation = Path("C:/Users/benja/Desktop/Mangas")

manga = "one-piece"
mangalocation = savelocation / manga
mangachapters = 967


def make_soup(url):
    thepage = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


Path.mkdir(mangalocation, parents=True, exist_ok=True)
for chapter in range(1, mangachapters + 1):
    chapterlocation = mangalocation / ("Chapter " + str(chapter))
    chapterlocation.mkdir(parents=True, exist_ok=True)

    page_exists = True
    page = 1
    try:
        while page_exists:
            soup = make_soup(base_url + '/' + manga + '/' + str(chapter) + '/' + str(page))

            image = ''
            for img in soup.findAll('img'):
                alt = img.get('alt')
                if (str(chapter) in alt) and (str(page) in alt):
                    image = img.get('src')

            print(image)

            imagefile = open(chapterlocation / ("Page " + str(page) + '.jpeg'), "wb")
            imagefile.write(urlopen(Request(image, headers={'User-Agent': 'Mozilla/5.0'})).read())
            imagefile.close()

            page += 1

    except urllib.error.HTTPError:
        print("End of chapter!")
