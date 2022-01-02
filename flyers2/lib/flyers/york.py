import os
import requests
import shutil
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


def get_flyers(url: str) -> dict:
    """
    ヨークマートのチラシのURLとダウンロードしたファイルパスをdictにして返す
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
