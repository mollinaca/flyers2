import requests
from bs4 import BeautifulSoup


def get_flyers_url(url: str) -> list:
    """
    ヨークマートチラシの店舗ページから、チラシ単位のURL一覧をリストで取得する
    """
    ret = []
    YORKMART_URL = "https://www.york-inc.com"
    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")
    leaflets = html.find_all(class_="leaflet pc")
    for leaflet in leaflets:
        for l2 in leaflet.findAll("img")[0].get("data-set").split(","):
            if "jpg" in l2:
                ret.append(YORKMART_URL + l2)

    return ret
