import os
import requests
from bs4 import BeautifulSoup
from pdf2image import convert_from_path


def get_flyers_url(url: str) -> list:
    """
    ロヂャースの店舗のチラシページからチラシpdfのURLを取得する
    """
    ret = []
    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")
    sid = html.find_all("script")[6].get("src").split("=")[1]

    # ロヂャースマート大和田
    id = "16613006"
    eid = "18bca89dc7cd51c5d2f3c4470ceea028"
    url = "https://cms.mechao.tv/rogers/viewer?id=" + id + "&eid=" + eid + "&sid=" + sid

    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")
    script_ele = html.find_all("script")[12].prettify().split(";")
    for s in script_ele:
        if "Pdf" in s:
            s2 = s
            break

    for s in s2.splitlines():
        if "https://" in s:
            ret = s.split("=")[1].replace(" ", "").replace("'", "")
            break

    print(ret)
    return ret


def get_flyers_urls(url: str) -> list:
    ret = get_flyers_url(url)
    return ret


def get_flyers(url: str) -> dict:
    """
    ロヂャースのチラシのURLとダウンロードしたファイルパスをdictにして返す
    ret: {ret[flyer_url]:flyer_filepath,}
    """
    ret = {}
    pdf_url = get_flyers_url(url)
    d = str(pdf_url.split("/")[-2])
    filename = "rogers-" + d + ".pdf"
    res = requests.get(pdf_url, stream=True)
    with open(filename, mode="wb") as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    images = convert_from_path(filename)
    ret_images = []
    for i, image in enumerate(images):
        filename_png = "rogers-" + d + "-" + str(i) + ".png"
        image.save(filename_png, "PNG")
        ret_images.append(filename_png)

    os.remove(filename)
    ret[url] = ret_images
    return ret
