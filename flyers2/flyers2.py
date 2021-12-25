def hello(name):
    print("Hello, %s!" % name)


def main():
    # 自分テスト用
    #    from .lib import libtest as lt
    from .lib import libtest
    from .lib.flyers import testshop, york

    hello("test")
    libtest.libtestf()

    ###################
    #  メイン処理 #
    ###################

    #  module import #
    import configparser
    import json
    import pathlib

    # valiables #
    here = pathlib.Path(__file__).resolve().parent
    #    CONFIG_FILE = str(here) + "/config.ini"
    CONFIG_FILE = str(here) + "/config_dev.ini"  # dev mode

    #  設定の読み込み #
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)
    print(cfg.sections())
    print(cfg["notify"]["slack_webhook"])

    # 前回データ取得

    # 店舗単位処理

    shop_urls = json.loads(cfg["target"]["shops"])
    for shop_url in shop_urls:
        print(shop_url)

        # shop_url ごとの分岐
        if "test-shopurl" in shop_url:  # 開発用
            flyers = testshop.get_testshop_flyers(shop_url)
            print(flyers)

        elif "york" in shop_url:
            york.yorkf()

        else:
            pass

    hello("end")


if __name__ == "__main__":
    main()
