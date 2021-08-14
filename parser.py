import requests
from bs4 import BeautifulSoup


URL = "https://7karat.by/catalog/koltsa/"
KORAT_PAGE = requests.get(URL)

SOUP = BeautifulSoup(KORAT_PAGE.content, "html.parser")


def get_rings():
    return SOUP.find_all("div", class_="one_product_js")


def get_ring_params(ring_soup, link):
    articul = ring_soup.find_all("td", itemprop="brand")[0].contents[0]
    material = ring_soup.find_all("label", class_="size-radio-label")[0].contents[0]
    ring_type = link.split("/")[3]

    return articul, material, ring_type


def get_probe(ring_soup):
    probe_classes = ring_soup.find_all("td", class_="proba-value")

    if len(probe_classes) == 2:
        probe = ring_soup.find_all("td", class_="proba-value")[1].contents[0]
    else:
        probe = ring_soup.find_all("td", class_="proba-value")[0].contents[0]
    
    return probe


def get_shops(ring_soup):
    return ring_soup.find_all("div", class_="info_city_content")


def get_shop_param(shop):
    weight_blocks = shop.find_all("div", class_="weight-block")
    prices = shop.find_all("span", itemprop="price")

    weight_spans = weight_blocks[0].find_all("span")

    weight = weight_spans[0].contents[0]
    size = weight_spans[1].contents[0]
    price = prices[0].contents[0]
    defect = len(shop.find_all("div", class_="info_text")[0].contents) == 1

    return weight, size, price, defect


if __name__ == "__main__":
    DATA_FILE = open("data.txt", "w", encoding="utf-8")

    for ring in get_rings():
        link = ring.find("a", class_="link_to_product")["href"]
        ring_page = requests.get(f"https://7karat.by/{link}")
        ring_soup = BeautifulSoup(ring_page.content, "html.parser")

        articul, material, ring_type = get_ring_params(ring_soup, link)
        probe = get_probe(ring_soup)

        for shop in get_shops(ring_soup):
            weight, size, price, defect = get_shop_param(shop)
            print(f"{articul},{material},{weight},{size},{defect},{probe},{ring_type},{price}")
            DATA_FILE.write(f"{articul};{material};{weight};{size};{int(defect)};{probe};{ring_type};{price}\n")

    DATA_FILE.close()
