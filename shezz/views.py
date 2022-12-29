from types import NoneType
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml import html
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

ZAFUL_TOPS_URL = 'https://es.zaful.com/tops-e_6/'
ZAFUL_ITEM_URL = 'https://es.zaful.com/top-corta-con-cuello-en-u-puid_5049121.html?kuid=1178194'

SHEIN_TOPS_CONTAINER = 'product-list-v2__container'
SHEIN_TOP_ITEM = 'S-product-item j-expose__product-item product-list__item'


# Create your views here.
def home(request):
    return render(request, "base.html")

def scrapp(request):
    if request.method == 'POST':
        shein_tops()
    return render(request, "scrapp/scrapp.html")


def shein_single_product(product_url):
    url = ZAFUL_ITEM_URL
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    info_container = soup.find("div", {"class": "product-intro__head j-expose__product-intro__head"})
    print(info_container.prettify())


def shein_tops():
    shein_tops = []
    path = '/Users/jvegax/projects/python/shezz-env/shezz-repo/shezz/data/shein-data/tops-shein-page.html' 
    
    with open(path, 'r') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_container = soup.find("div", {"class": SHEIN_TOPS_CONTAINER})
        products = product_container.find_all("section", {"class": SHEIN_TOP_ITEM})
        
        mensaje = '🟢 Se han encontrado: ' + format(len(products)) + ' productos'
        print(mensaje)
        counter = 0

        for product in products:
            if counter == 12:
                break

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
            # print(name)
            
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
            PROUCT_PRICE_CLASS_2 = 'normal-price-ctn__sale-price'
            prouct_price = product_item_prices.find("span", {"class": PROUCT_PRICE_CLASS})
            prouct_price_2 = product_item_prices.find("span", {"class": PROUCT_PRICE_CLASS_2})
                
            # Product discount price
            PROUCT_DISCOUNT_PRICE_CLASS = 'normal-price-ctn__sale-price normal-price-ctn__sale-price_promo'
            prouct_discount_price = product_item_prices.find("span", {"class": PROUCT_DISCOUNT_PRICE_CLASS})
            
            if prouct_price is not None:
                price = prouct_price.text
            elif prouct_price_2 is not None:
                price = prouct_price_2.text

            if prouct_discount_price is not None:
                price_discount = prouct_discount_price.text

            print(f"🟢 Nombre: {name} Precio: {price}, Precio descuento: {price_discount}")
        
            counter += 1
            
    return shein_tops

# This function recives a product soup and returns the product price and discount price
def find_price(product_soup):
    pass