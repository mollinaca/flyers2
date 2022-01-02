import os
import requests
import shutil
from bs4 import BeautifulSoup


def get_flyers_url(url: str) -> list:
    ret = []

    tokubai_url = "https://tokubai.co.jp"
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
          (KHTML, like Gecko) Chrome/69.0.3497.100"
    headers = {"User-Agent": ua}
    res = requests.get(url, headers=headers)
    html = BeautifulSoup(res.content, "html.parser")

    # leaflet_component がない場合、掲載チラシがないので終了する
    if not html.findAll(class_="leaflet_component"):
        return ret

    leaflet_page_url = tokubai_url + html.findAll(class_="leaflet_component")[0].find(
        class_="image_element"
    ).get("href")

    res = requests.get(leaflet_page_url, headers=headers)
    html = BeautifulSoup(res.content, "html.parser")
    leaflet_page_link = html.find_all(class_="other_leaflet_link")

    leaflet_page_links = []
    for link_url in leaflet_page_link:
        leaflet_page_links.append(tokubai_url + link_url.get("href").split("?")[0])

    for url in leaflet_page_links:
        res = requests.get(url, headers=headers)
        html = BeautifulSoup(res.content, "html.parser")
        ret.append(html.find(class_="leaflet").get("src").split("?")[0])

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
