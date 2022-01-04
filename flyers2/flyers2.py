import configparser
import json
import os
import pathlib
import time
from .lib.flyers import york, kurashiru, tokubai
from .lib.notify import slack


def main():

    here = pathlib.Path(__file__).resolve().parent
    CONFIG_FILE = str(here) + "/config.ini"
    # CONFIG_FILE = str(here) + "/config_dev.ini"  # for development

    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)
    SLACK_BOT_TOKEN = cfg["notify"]["slack_bot_token"]
    SLACK_CHANNEL = cfg["notify"]["slack_channel"]

    if not os.path.exists("last.json"):
        last_flyers = []
    else:
        json_open = open("last.json", "r")
        last = json.load(json_open)
        last_flyers = last["flyers"]
    new_flyers = []
    new_time = time.time()

    shop_urls = json.loads(cfg["target"]["shops"])
    for shop_url in shop_urls:

        if "test-shopurl" in shop_url:  # for development
            pass

        elif "york" in shop_url or "kurashiru" in shop_url or "tokubai" in shop_url:
            if "york" in shop_url:
                flyers = york.get_flyers(shop_url)
            elif "kurashiru" in shop_url:
                flyers = kurashiru.get_flyers(shop_url)
            elif "tokubai" in shop_url:
                flyers = tokubai.get_flyers(shop_url)
            else:
                continue

            for flyer_url, img_path in flyers.items():
                if img_path not in last_flyers:
                    response = slack.file_upload(
                        SLACK_BOT_TOKEN, SLACK_CHANNEL, img_path, flyer_url
                    )
                    if response["ok"]:
                        new_flyers.append(img_path)
                    else:
                        # 60 sec sleep and retry only once
                        time.sleep(60)
                        response = slack.file_upload(
                            SLACK_BOT_TOKEN, SLACK_CHANNEL, img_path, flyer_url
                        )
                        if response["ok"]:
                            new_flyers.append(img_path)
                        else:
                            pass
                            # if fail twice, give up
                os.remove(img_path)

        else:
            pass

    new_flyers_json = {"time": new_time, "flyers": new_flyers}
    with open("last.json", "w") as f:
        json.dump(new_flyers_json, f, indent=4)


if __name__ == "__main__":
    main()
