from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context


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

