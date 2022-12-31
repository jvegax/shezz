# Descripcion: Este script almacena +2000 tops de Shein en un archivo JSON

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import ssl
import json

# Deshabilita la verificación de certificados SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Crea una instancia del servicio de ChromeDriver con la ruta al ejecutable
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
service = Service(CHROME_DRIVER_PATH)

ZAFUL_TOPS_LINKS_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/zaful/links.json'
ZAFUL_TOPS_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/zaful/zaful-tops.json'

ZAFUL_ITEM_NAME_CLASS = 'js-goods-title goods-text'  # h1
ZAFUL_ITEM_SKU_CLASS = 'sku'  # p > find first span > get text value (sku)
ZAFUL_ITEM_RATING_CLASS = 'ml10 js-rate-all'  # p > get text value (rating)

# Prices
# span > get text value (discount)
ZAFUL_OFFER_ITEM_DISCOUNT_CLASS = 'shop-price my_shop_price js-new-price'
ZAFUL_OFFER_ITEM_DISCOUNT_CLASS_V2 = 'shop-price my_shop_price js-new-price color_tag'
# strong > get text value (original price)
ZAFUL_OFFER_ITEM_ORIGINAL_PRICE_CLASS = 'my_shop_price js_market_wrap js-match-origin_price'

# Sizes
ZAFUL_ITEM_SIZE_CLASS = 'js-sizeItem'  # p > findAll > get text value (sizes)

# findAll > get src value (image)
# div > find ul  > findAll li > find image > get src value (images)
ZAFUL_ITEM_IMAGES_CONTAINER = 'goods-gallery-thumb fl'
ZAFUL_ITEM_IMAGE_CLASS = 'js_loadingimg'

# ***************************************************************************************************


def normalize_price(price):
    return price.replace("PVP ", "")


ALL_ZAFUL_TOPS = []

# Abre el archivo links.json en modo lectura
with open(ZAFUL_TOPS_LINKS_PATH, 'r') as file:
    links = json.load(file)
    counter = 0

    # Itera sobre cada enlace
    for link in links:
        if counter == 1000:
            break
        NEW_ZAFUL_TOP = {}

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
        category = 'tops'
        rating = 'unknown'
        product_link = link
        sizes = []
        images = []

        # Name
        name_soup = soup.find("h1", {"class": ZAFUL_ITEM_NAME_CLASS})
        if name_soup:
            name = name_soup.text.strip()

        # SKU
        sku_soup = soup.find("p", {"class": ZAFUL_ITEM_SKU_CLASS})
        if sku_soup:
            sku_soup_span = sku_soup.find('span')
            if sku_soup_span:
                sku = sku_soup_span.text.strip()

        # Rating
        rating_soup = soup.find(
            "p", {"class": ZAFUL_ITEM_RATING_CLASS})
        if rating_soup:
            rating = rating_soup.text.strip()

        # Price
        price_discount_soup = soup.find(
            "span", {"class": ZAFUL_OFFER_ITEM_DISCOUNT_CLASS})
        if price_discount_soup:
            price_discount = price_discount_soup.text.strip()
        else:
            price_discount_soup = soup.find(
                "span", {"class": ZAFUL_OFFER_ITEM_DISCOUNT_CLASS_V2})
            if price_discount_soup:
                price_discount = price_discount_soup.text.strip()

        # Get original price
        price_original_soup = soup.find(
            "strong", {"class": ZAFUL_OFFER_ITEM_ORIGINAL_PRICE_CLASS})
        if price_original_soup:
            price_original_raw = price_original_soup.text.strip()
            price_original = normalize_price(price_original_raw)

        # Sizes
        sizes_soup = soup.findAll("p", {"class": ZAFUL_ITEM_SIZE_CLASS})
        if sizes_soup:
            for size in sizes_soup:
                sizes.append(size.text.strip())

        # Images
        images_container_soup = soup.find("div", {"class": ZAFUL_ITEM_IMAGES_CONTAINER})
        if images_container_soup:
            images_ul_soup = images_container_soup.find("ul")
            if images_ul_soup:
                images_li_soup = images_ul_soup.findAll("li")
                if images_li_soup:
                    for image_li in images_li_soup:
                        image_soup = image_li.find("img", {"class": ZAFUL_ITEM_IMAGE_CLASS})
                        if image_soup:
                            images.append(image_soup['src'])
        
        # Guardamos los datos en un diccionario
        NEW_ZAFUL_TOP = {
            'sku': sku,
            'name': name,
            'price_discount': price_discount,
            'price_original': price_original,
            'category': category,
            'rating': rating,
            'product_link': product_link,
            'sizes': sizes,
            'images': images
        }
        ALL_ZAFUL_TOPS.append(NEW_ZAFUL_TOP)
        print(f'✨ New product added ({counter+1}) ✨')
        counter += 1

    # Cerramos el driver
    # Close driver and links file
    driver.close()
    driver.quit()

# Abrir un archivo para escritura
with open(ZAFUL_TOPS_PATH, 'w') as tops_file:
    json.dump(ALL_ZAFUL_TOPS, tops_file, indent=2)
