"""
for development mode
"""


def get_testshop_flyers_pages(url: str) -> list:
    ret = [
        "https://test-shopurl.example.com/flyers/flyers1",
        "https://test-shopurl.example.com/flyers/flyers",
    ]
    return ret


def get_testshop_flyers_images(pages: str) -> list:
    ret = []
    for page in pages:
        img_url = page + "/img.png"
        ret.append(img_url)
    return ret


def get_testshop_flyers(url: str):
    pages = get_testshop_flyers_pages(url)
    imgs = get_testshop_flyers_images(pages)
    return [pages, imgs]
