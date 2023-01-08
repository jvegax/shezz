# Descripcion: Este script obtiene los links de +2000 tops de Shein

from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context

CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
LINKS_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/zaful/links-tops-zaful.json'

ZAFUL_TOPS_CONTAINER_CLASS = 'proList clearfix goods-proList-b'  # div
ZAFUL_TOPS_UL_CLASS = 'clearfix'  # ul inside div
ZAFUL_TOP_LI_CLASS = 'js_proList_item logsss_event_ps'  # li
ZAFUL_ITEM_LINK_CLASS = 'pic js_list_link pr logsss_event_cl'  # a inside li

PAGES = 35


# Abrimos el archivo en modo escritura
links = []
for page in range(1, PAGES+1):
    ZAFUL_TOPS_URL = f'https://es.zaful.com/tops-e_6/g_{page}.html'
    print(f"🚀 Pagina: {str(page)}")

    # Driver configuration
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(
        executable_path=CHROME_DRIVER_PATH, options=options)
    driver.get(ZAFUL_TOPS_URL)

    # Scraping
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    zaful_tops_container = soup.find(
        "div", {"class": ZAFUL_TOPS_CONTAINER_CLASS})

    zaful_tops_ul_soup = zaful_tops_container.find(
        "ul", {"class": ZAFUL_TOPS_UL_CLASS})

    products = zaful_tops_ul_soup.find_all(
        "li", {"class": ZAFUL_TOP_LI_CLASS})

    for product in products:
        link = '#'  # Default value
        link_soup = product.find("a", {"class": ZAFUL_ITEM_LINK_CLASS})
        if link_soup:
            link = link_soup['href']
        links.append(link)
        
    # Close driver and links file
    driver.close()
    driver.quit()


# Write links to file
with open(LINKS_PATH, 'w') as file:
    json.dump(links, file, indent=4)
