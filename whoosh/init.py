# Descripcion: este script genera el indice de whoosh

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import json, shutil, os, sys

arguments = sys.argv
SHEIN_INDEX_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/whoosh/Index'
SHEIN_TOPS_DATA_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/shein/tops-shein.json'
ALL_PRODUCTS_DATA_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/all-products.json'

# Creamos un esquema para nuestros documentos
def create_index():
    schema = Schema(
        name=TEXT(stored=True, phrase=False),
        sku = ID(stored=True),
        price_discount=TEXT(stored=True),
        price_original=TEXT(stored=True),
        category=TEXT(stored=True),
        rating=TEXT(stored=True),
        product_link=TEXT(stored=True),
        sizes=TEXT(stored=True),
        images=TEXT(stored=True)
    )
    
    if os.path.exists(SHEIN_INDEX_PATH):
        shutil.rmtree(SHEIN_INDEX_PATH)
    os.mkdir(SHEIN_INDEX_PATH)

    # Creamos un índice en un directorio llamado "shein_index"
    shein_ix = create_in(SHEIN_INDEX_PATH, schema)
    writer = shein_ix.writer()

    with open(SHEIN_TOPS_DATA_PATH, "r") as tops_file:
        obj_list = json.load(tops_file)
        for obj in obj_list:
            writer.add_document(
                name=obj["name"],
                sku=obj["sku"],
                price_discount=obj["price_discount"],
                price_original=obj["price_original"],
                category=obj["category"],
                rating=obj["rating"],
                product_link=obj["product_link"],
                sizes=obj["sizes"],
                images=obj["images"]
            )
        writer.commit()

create_index()