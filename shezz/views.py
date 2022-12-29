
import json
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
from django.shortcuts import render
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


SHEIN_HOST = 'https://es.shein.com'
LINKS_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/shezz/data/links.json'

PAGES = 5
SHEIN_TOPS_URL = 'https://es.shein.com/Women-Tops,-Blouses-Tee-c-1766.html?ici=es_tab01navbar04menu02&scici=navbar_WomenHomePage~~tab01navbar04menu02~~4_2~~real_1766~~~~0&src_module=topcat&src_tab_page_id=page_goods_detail1672330485398&src_identifier=fc%3DWomen%60sc%3DROPA%60tc%3DTOPS%60oc%3D0%60ps%3Dtab01navbar04menu02%60jc%3Dreal_1766&srctype=category&userpath=category-ROPA-TOPS'

# Create your views here.


def home(request):
    return render(request, "base.html")


def scrapp(request):
    if request.method == 'POST':
        scrap_links(SHEIN_TOPS_URL, PAGES)
    return render(request, "scrapp/scrapp.html")


def scrap_links(TOPS_URL, NUM_PAGES):

    for current_page in range(0, NUM_PAGES):
        # Constants
        SHEIN_TOPS_CONTAINER_CLASS = 'product-list j-expose__product-list j-product-list-info j-da-event-box'
        SHEIN_TOP_ITEM_CLASS = 'S-product-item j-expose__product-item product-list__item'
        SHEIN_ITEM_LINK_CLASS = 'S-product-item__img-container j-expose__product-item-img'

        # Driver configuration
        options = ChromeOptions()
        options.headless = True
        driver = Chrome(
            executable_path='/usr/local/bin/chromedriver', options=options)
        driver.get(f'{TOPS_URL}&page={str(current_page)}')

        # Scraping
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        shein_tops_container = soup.find(
            "div", {"class": SHEIN_TOPS_CONTAINER_CLASS})
        products = shein_tops_container.find_all(
            "section", {"class": SHEIN_TOP_ITEM_CLASS})
        print(f"🚀 Se han encontrado: {len(products)} productos")

        # Extract link from each product
        links = []
        for product in products:
            link = '#'  # Default value
            link_soup = product.find("a", {"class": SHEIN_ITEM_LINK_CLASS})
            if link_soup:
                link = SHEIN_HOST + link_soup['href']
            links.append(link)

        # Abrimos el archivo en modo escritura
        with open(LINKS_PATH, 'w') as file:
            # Escribe la lista de enlaces en el archivo en formato json
            json.dump(links, file, indent=4)

        # Close driver and links file
        driver.close()
        driver.quit()
