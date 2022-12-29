from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

SHEIN_TOPS = 'https://es.shein.com/Women-Tops,-Blouses-Tee-c-1766.html?ici=es_tab01navbar04menu02&scici=navbar_WomenHomePage~~tab01navbar04menu02~~4_2~~real_1766~~~~0&src_module=topcat&src_tab_page_id=page_real_class1672313857342&src_identifier=fc%3DWomen%60sc%3DROPA%60tc%3DTOPS%60oc%3D0%60ps%3Dtab01navbar04menu02%60jc%3Dreal_1766&srctype=category&userpath=category-ROPA-TOPS&child_cat_id=2223'

PRODUCT_CONTAINER = 'product-list-v2__container'
PRODUCT_INFO = 'S-product-item j-expose__product-item product-list__item'


# Create your views here.
def home(request):
    return render(request, "base.html")

def scrapp(request):
    if request.method == 'POST':
        shein_tops()
    return render(request, "scrapp/scrapp.html")

def shein_tops():
    url = SHEIN_TOPS
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    product_container = soup.find("div", {"class": PRODUCT_CONTAINER})
    products = product_container.find_all("section", {"class": PRODUCT_INFO})
    mensaje = '🟢 Se han encontrado: ' + format(len(products)) + ' productos'
    print(mensaje)
