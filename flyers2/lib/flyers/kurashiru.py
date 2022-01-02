import os
import requests
import shutil
from bs4 import BeautifulSoup


def get_flyers_url(url: str) -> list:
    ret = []
    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")
    leaflets = html.findAll("img", class_="StoresShow-leafletImage is-vertical")
    for leaflet in leaflets:
        ret.append(leaflet["src"])

    return ret


def get_flyers(url: str) -> dict:
    ret = {}
    flyer_urls = get_flyers_url(url)
    for url in flyer_urls:
        filename = os.path.basename(url)
        res = requests.get(url, stream=True)
        with open(filename, mode="wb") as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)
        ret[url] = filename

    return ret
