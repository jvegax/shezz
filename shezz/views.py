from types import NoneType
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

SHEIN_TOPS = 'https://es.shein.com/Women-Tops,-Blouses-Tee-c-1766.html?ici=es_tab01navbar04menu02&scici=navbar_WomenHomePage~~tab01navbar04menu02~~4_2~~real_1766~~~~0&src_module=topcat&src_tab_page_id=page_real_class1672313857342&src_identifier=fc%3DWomen%60sc%3DROPA%60tc%3DTOPS%60oc%3D0%60ps%3Dtab01navbar04menu02%60jc%3Dreal_1766&srctype=category&userpath=category-ROPA-TOPS&child_cat_id=2223'

SHEIN_TOPS_CONTAINER = 'product-list-v2__container'
SHEIN_TOP_ITEM = 'S-product-item j-expose__product-item product-list__item'


# Create your views here.
def home(request):
    return render(request, "base.html")

def scrapp(request):
    if request.method == 'POST':
        shein_tops()
    return render(request, "scrapp/scrapp.html")

def shein_tops():
    
    shein_tops = []
    names = []
    
    url = SHEIN_TOPS
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    product_container = soup.find("div", {"class": SHEIN_TOPS_CONTAINER})
    products = product_container.find_all("section", {"class": SHEIN_TOP_ITEM})
    mensaje = '🟢 Se han encontrado: ' + format(len(products)) + ' productos'
    print(mensaje)
    
    for product in products:

        name = ''
        price = ''
        price_discount = ''
        category = ''
        sizes = []
        rating = ''
        link = ''
        image = ''
        brand = ''
        
        # Product name
        name = product['aria-label']
        
        # Product price and discount containers
        PRODUCT_ITEM_INFO_CLASS = 'S-product-item__info'
        product_item_info = product.find("div", {"class": PRODUCT_ITEM_INFO_CLASS})
        
        PRODUCT_ITEM_PRICE_CONTAINER_CLASS = 'S-product-item__price'
        product_item_price_container = product_item_info.find("div", {"class": PRODUCT_ITEM_PRICE_CONTAINER_CLASS})
        
        PRODUCT_ITEM_PRICE_SECTION_CLASS = 'normal-price-ctn normal-price-ctn__height-holder'
        product_item_price_section = product_item_price_container.find("section", {"class": PRODUCT_ITEM_PRICE_SECTION_CLASS})

        PRODUCT_ITEM_PRICES_CLASS = 'normal-price-ctn__prices normal-price-ctn__prices_gap'
        product_item_prices = product_item_price_section.find("div", {"class": PRODUCT_ITEM_PRICES_CLASS})
        
        # Product price
        PROUCT_PRICE_CLASS = 'normal-price-ctn__retail-price'
        prouct_price = product_item_prices.find("span", {"class": PROUCT_PRICE_CLASS})
        
        # Product discount price
        PROUCT_DISCOUNT_PRICE_CLASS = 'normal-price-ctn__sale-price normal-price-ctn__sale-price_promo'
        prouct_discount_price = product_item_prices.find("span", {"class": PROUCT_DISCOUNT_PRICE_CLASS})
        
        # Normalizing prices
        if prouct_price:
            price = prouct_price.text
        else:
            price = 'unknown'
        if prouct_discount_price:
            price_discount = prouct_discount_price.text
        else:
            price_discount = 'unknown'
        
        print('🟢 Nombre: ' + name, ' - Precio: ' + price, ' - Precio con descuento: ' + price_discount)

            
    return shein_tops

# This function recives a product soup and returns the product price and discount price
def find_price(product_soup):
    pass