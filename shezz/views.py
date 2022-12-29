
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions


SHEIN_TOPS_URL = 'https://es.shein.com/Women-Tops,-Blouses-Tee-c-1766.html?ici=es_tab01navbar04menu02&scici=navbar_WomenHomePage~~tab01navbar04menu02~~4_2~~real_1766~~~~0&src_module=topcat&src_tab_page_id=page_goods_detail1672330485398&src_identifier=fc%3DWomen%60sc%3DROPA%60tc%3DTOPS%60oc%3D0%60ps%3Dtab01navbar04menu02%60jc%3Dreal_1766&srctype=category&userpath=category-ROPA-TOPS'


# Create your views here.
def home(request):
    return render(request, "base.html")

def scrapp(request):
    if request.method == 'POST':
        shein_test(SHEIN_TOPS_URL)
    return render(request, "scrapp/scrapp.html")


def shein_test(tops_url):
    # Constants
    SHEIN_TOPS_CONTAINER_CLASS = 'product-list j-expose__product-list j-product-list-info j-da-event-box'
    SHEIN_TOP_ITEM_CLASS = 'S-product-item j-expose__product-item product-list__item'
    SHEIN_ITEM_NAME_CLASS = 'S-product-item__link_jump S-product-item__link'
    
    # Driver configuration
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    driver.get(tops_url)
    
    # Scraping
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    shein_tops_container = soup.find("div", {"class": SHEIN_TOPS_CONTAINER_CLASS})
    products = shein_tops_container.find_all("section", {"class": SHEIN_TOP_ITEM_CLASS})
    print(f"🚀 Se han encontrado: {len(products)} productos")
    
    for product in products: 
        price = ''
        name = ''

        # Name
        name = product.find("a", {"class": SHEIN_ITEM_NAME_CLASS}).text
       
        # Prices
        price_soup = product.find("span", {"class": "normal-price-ctn__sale-price normal-price-ctn__sale-price_promo"})
        price_soup_2 = product.find("span", {"class": "normal-price-ctn__sale-price"})
        if price_soup is not None:
            price = price_soup.text
        elif price_soup_2 is not None:
            price = price_soup_2.text
            
        print(f"👗 {name} - {price}")