# Descripcion: Este script combina los datos de dos archivos .json en uno solo

import json
import random


SHEIN_TOPS_FILE_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/shein/tops-shein.json'
ZAFUL_TOPS_FILE_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/zaful/zaful-tops.json'
SAVE_FILE_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/all-products.json'

# Abrimos ambos archivos .json y los cargamos en variables
with open(SHEIN_TOPS_FILE_PATH, "r") as f:
    shein_tops = json.load(f)

with open(ZAFUL_TOPS_FILE_PATH, "r") as f:
    zaful_tops = json.load(f)

# Creamos una nueva estructura de datos que combina los datos de ambos archivos
combined_data = shein_tops + zaful_tops

# Desordenamos la lista de datos combinada
random.shuffle(combined_data)

# Normalizamos los precios para poder realizar busqueda con whoosh de rango
for product in combined_data:
    price_discount = product["price_discount"]
    price_original = product["price_original"]
    
    #     "price_discount": "unknown" replace to "price_discount": 0.0 
    if price_discount == "unknown":
        price_discount = "0.0"
    
    # Elimina el símbolo del euro de price_discount y price_original
    product["price_discount"] = float(price_discount.replace("€", "").replace(",", "."))
    product["price_original"] = float(price_original.replace("€", "").replace(",", "."))
    # Añade la propiedad currency y asigna a esta propiedad el valor "eur"
    product["currency"] = "eur"

# Escribimos la estructura de datos combinada a un nuevo archivo .json
with open(SAVE_FILE_PATH, "w") as f:
    json.dump(combined_data, f, indent=4)
