# Description: Este script obtiene info de +2000 tops de Shein

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import ssl
import json
import re

# Deshabilita la verificación de certificados SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Crea una instancia del servicio de ChromeDriver con la ruta al ejecutable
service = Service('/usr/local/bin/chromedriver')

SHEIN_TOPS_LINKS_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/links-tops-shein.json'

SHEIN_ITEM_NAME_CLASS = 'product-intro__head-name'  # h1
SHEIN_ITEM_SKU_CLASS = 'product-intro__head-sku'  # div
# div > find firts span > get aria-label value (rating)
SHEIN_ITEM_RATING_CONTAINER_CLASS = 'product-intro__head-reviews'

# Case product has discount
# div > find first span > get text value (discount)
SHEIN_OFFER_ITEM_DISCOUNT_CLASS = 'discount'
# del > get text value (original price)
SHEIN_OFFER_ITEM_ORIGINAL_PRICE_CLASS = 'del-price'

# Case product has no discount
SHEIN_ITEM_PRICE = 'original'  # div > find first span > get text value (price)

# Sizes
# findAll > div > get text value (size)
SHEIN_ITEM_SIZE_CLASS = 'product-intro__size-radio-inner'

# findAll > get src value (image)
SHEIN_ITEM_IMAGE_CLASS = 'j-verlok-lazy loaded'

# ***************************************************************************************************


def normalize_rating(raw_rating):
    match = re.search(r"Valoración media\s([0-9.]+)", raw_rating)
    rating = match.group(1)
    return rating.strip()


# Abre el archivo links.json en modo lectura
with open(SHEIN_TOPS_LINKS_PATH, 'r') as file:
    # Carga el contenido del archivo en una variable
    links = json.load(file)

# Itera sobre cada enlace
for link in links:

    # Driver configuration
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(
        executable_path='/usr/local/bin/chromedriver', options=options)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Scraping
    sku = ''
    name = ''
    price_discount = ''
    price_original = ''
    category = ''
    rating = ''
    product_link = link
    sizes = []
    images = []

    # Name
    name_soup = soup.find("h1", {"class": SHEIN_ITEM_NAME_CLASS})
    if name_soup:
        name = name_soup.text.strip()

    # SKU
    sku_soup = soup.find("div", {"class": SHEIN_ITEM_SKU_CLASS})
    if sku_soup:
        sku = sku_soup.text.strip()

    # Rating
    rating_soup = soup.find(
        "div", {"class": SHEIN_ITEM_RATING_CONTAINER_CLASS})
    if rating_soup:
        rating_span_soup = rating_soup.find('span')  # .get('aria-label')
        if rating_span_soup:
            text = rating_span_soup.get('aria-label')
            rating = normalize_rating(text)

    # Price
    price_original_soup = soup.find(
        "div", {"class": SHEIN_ITEM_PRICE})
    if price_original_soup:
        price_original_span_soup = price_original_soup.find('span')
        if price_original_span_soup:
            price_original = price_original_span_soup.text.strip()
            price_discount = 'unknown'
    else:
        # Case product has discount

        # Get discount
        price_discount_soup = soup.find(
            "div", {"class": SHEIN_OFFER_ITEM_DISCOUNT_CLASS})
        if price_discount_soup:
            # find first span > get text value (discount)
            discount_span_soup = price_discount_soup.find('span')
            if discount_span_soup:
                price_discount = discount_span_soup.text.strip()
        # Get original price
        price_original_soup = soup.find(
            "del", {"class": SHEIN_OFFER_ITEM_ORIGINAL_PRICE_CLASS})
        if price_original_soup:
            price_original = price_original_soup.text.strip()
    
    print(f'✨ {sku} - {rating} - Descuento: {price_discount} - Precio original: {price_original}')
