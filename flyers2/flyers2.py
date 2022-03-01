import configparser
import json
import os
import pathlib
import requests
import shutil
import time
from pdf2image import convert_from_path
from .lib.flyers import york, yaoko, kurashiru, tokubai, rogers
from .lib.notify import slack


def get_last_json() -> dict:
    _LAST_FLYERS_FILE = "last.json"

    if os.path.exists(_LAST_FLYERS_FILE):
        if os.path.getsize(_LAST_FLYERS_FILE) == 0:
            ret = []
        else:
            json_open = open(_LAST_FLYERS_FILE, "r")
            last = json.load(json_open)
            ret = last["flyers"]
    else:
        ret = []

    return ret


def update_last_json(t: time, flyers: list):
    _LAST_FLYERS_FILE = "last.json"
    new_flyers_json = {"time": t, "flyers": flyers}
    with open(_LAST_FLYERS_FILE, "w") as f:
        json.dump(new_flyers_json, f, ensure_ascii=False, indent=4)

    return 0


def dl(url: str) -> str:
    """
    download the file and return filename
    """
    filename = os.path.basename(url)
    if 64 < len(filename):
        filename = filename[:60] + filename.split(".")[-1]
    res = requests.get(url, stream=True)
    with open(filename, mode="wb") as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)

    return filename


# def pdf2png(filename: str) -> list:
#    """
#    pdf ファイルを必要なだけ分割したpngのファイルリストで返す
#    """
#    ret = []
#    print(filename)
#    exit()
#
#    d = str(pdf_url.split("/")[-2])
#    res = requests.get(pdf_url, stream=True)
#    with open(filename, mode="wb") as f:
#        for chunk in res.iter_content(chunk_size=1024):
#            if chunk:
#                f.write(chunk)
#
#    images = convert_from_path(filename)
#    ret_images = []
#    for i, image in enumerate(images):
#        filename_png = "rogers-" + d + "-" + str(i) + ".png"
#        image.save(filename_png, "PNG")
#        ret_images.append(filename_png)
#
#    os.remove(filename)
#    ret[url] = ret_images
#    return ret


def get_flyers_urls(shop_urls: dict) -> dict:
    ret = {}

    for shop_name, shop_url in shop_urls.items():
        if "test-shopurl" in shop_url:  # for development
            pass

        elif "york" in shop_url:
            flyers = york.get_flyers_url(shop_url)

        elif "yaoko-net" in shop_url:
            flyers = yaoko.get_flyers_url(shop_url)

        elif "rogers" in shop_url:
            flyers = rogers.get_flyers_urls(shop_url)

        elif "kurashiru" in shop_url:
            flyers = kurashiru.get_flyers_url(shop_url)

        elif "tokubai" in shop_url:
            flyers = tokubai.get_flyers_url(shop_url)

        else:
            continue

        for flyer in flyers:
            ret[shop_name] = flyers

    return ret


def main():

    here = pathlib.Path(__file__).resolve().parent
    CONFIG_FILE = str(here) + "/config.ini"
    # CONFIG_FILE = str(here) + "/config_dev.ini"  # for development

    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)
    SLACK_BOT_TOKEN = cfg["notify"]["slack_bot_token"]
    SLACK_CHANNEL = cfg["notify"]["slack_channel"]

    last_flyers = get_last_json()
    new_flyers = []
    new_time = time.time()
    target_shops = json.loads(cfg["target"]["shops"])

    # shop_urls の内容から、取得されるチラシファイルのURL一覧を作成する処理
    flyers_urls = get_flyers_urls(target_shops)

    # すでに取得済みのチラシリストと、新規で取得するチラシのURLリストを作る
    new_flyers = {}
    target_flyers = {}
    for k, v in flyers_urls.items():
        if k in last_flyers:
            new_flyers[k] = list(set(v) & set(last_flyers[k]))
            target_flyers[k] = list(set(v) - set(last_flyers[k]))
        else:
            target_flyers[k] = v
            new_flyers[k] = []

    # すでに取得済みのため今回は取得しないチラシURL一覧を last_json に更新する
    update_last_json(new_time, new_flyers)

    for target_shop, flyer_urls in target_flyers.items():
        for flyer_url in flyer_urls:

            if "rogers" in flyer_url:
                # rogers 用の処理
                # ここにあるのも違う気がするなぁ・・・
                pass

            else:
                # 通常処理
                filename = dl(flyer_url)
                response = slack.file_upload2(
                    SLACK_BOT_TOKEN,
                    SLACK_CHANNEL,
                    filename,
                    target_shop + " : " + flyer_url,
                )
                if response["ok"]:
                    new_flyers[target_shop].append(flyer_url)
                    update_last_json(new_time, new_flyers)
                else:
                    # Todo: 失敗を通知したりする処理
                    pass

            os.remove(filename)


if __name__ == "__main__":
    main()
    exit()
