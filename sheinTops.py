# Description: Este script obtiene info de +2000 tops de Shein

from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

SHEIN_TOPS_LINKS_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/links-tops-shein.json'

SHEIN_ITEM_NAME_CLASS = 'product-intro__head-name' # h1
SHEIN_ITEM_SKU_CLASS = 'product-intro__head-sku' # div
SHEIN_ITEM_RATING_CONTAINER_CLASS = 'product-intro__head-reviews' # div > find firts span > get aria-label value (rating) 

# Case product has discount
SHEIN_OFFER_ITEM_DISCOUNT_CLASS = 'discount' # div > find first span > get text value (discount)
SHEIN_OFFER_ITEM_ORIGINAL_PRICE_CLASS = 'del-price' # del > get text value (original price)

# Case product has no discount
SHEIN_ITEM_PRICE = 'original' # div > find first span > get text value (price)

# Sizes 
SHEIN_ITEM_SIZE_CLASS = 'product-intro__size-radio-inner' # findAll > div > get text value (size)

SHEIN_ITEM_IMAGE_CLASS = 'j-verlok-lazy loaded' # findAll > get src value (image)

# ***************************************************************************************************

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
    product_link = ''
    sizes = []
    images = []
    
    