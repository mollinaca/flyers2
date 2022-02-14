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
    # print(html)
    script_ele = html.find_all("script")[12].prettify().split(";")
    for s in script_ele:
        if "Pdf" in s:
            s2 = s
            break

    for s in s2.splitlines():
        if "https://" in s:
            ret = s.split("=")[1].replace(" ", "").replace("'", "")
            break

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
