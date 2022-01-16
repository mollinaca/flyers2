import os
import requests
import shutil
from bs4 import BeautifulSoup


def get_flyers_url(url: str) -> list:
    """
    ヤオコーの店舗のチラシページからチラシURLを取得する
    """
    ret = []
    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")
    chirashi_page_link_url = (
        html.find(class_="section_description").find("a").get("href")
    )

    res = requests.get(chirashi_page_link_url)
    html = BeautifulSoup(res.content, "html.parser")

    c = html.find_all(class_="header_helper_nav")
    for c2 in c:
        ret.append(c2.find("a").get("href"))

    c = html.find_all(class_="otherFlyer_list_img")
    for c2 in c:
        ret.append(c2.find("img").get("src"))

    return ret


def get_flyers(url: str) -> dict:
    """
    YAOKOのチラシのURLとダウンロードしたファイルパスをdictにして返す
    ret: {ret[flyer_url]:flyer_filepath,}
    """
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
