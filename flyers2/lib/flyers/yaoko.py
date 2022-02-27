import requests
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
