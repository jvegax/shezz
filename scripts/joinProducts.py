# Descripcion: Este script combina los datos de dos archivos .json en uno solo

import json
import random

# Tallas normalizadas y sus variantes
sizes_dict = {
    "XXS": ["XXS", "Petite XXS(32)", "XXS(32)", "XXS-L", "XXS-S", "XXS-M", "XXS-XL", "XXS-XXL", "XXS-XXXL", 'XXS(32)', 'XXS(30)', 'XXS(34)'],
    "XS": ["XS", "Petite XS(34)", "XS(34)", "Tall XS(34)", "XS-L", "XS-S", "XS-M", "XS-XL", "XS-XXL", "XS-XXXL", 'XS(34)', 'XS(32)', 'XS(36)'],
    "S": ["S", "Petite S(36)", "Tall S(36)", "S-L", "S-S", "S-M", "S-XL", "S-XXL", "S-XXXL", 'S(36)', 'S(34)', 'S(38)', 'S(32)', 'S(40)'],
    "M": ["M", "Petite M(38)", 'M(34)', "Tall M(38)", "M-L", "M-S", "M-M", "M-XL", "M-XXL", "M-XXXL", 'M(38)', 'M(36)', 'M(40)'],
    "L": ["L", "Petite L(40/42)", "Tall L(40/42)", "L-L", "L-S", "L-M", "L-XL", "L-XXL", "L-XXXL", 'L(38)', 'L(40/42)', 'L(40)', 'L(42)', 'L(44)', 'L(36)'],
    "XL": ["XL", "Tall XL(44)", "XL-L", "XL-S", "XL-M", "XL-XL", "XL-XXL", "XL-XXXL", 'XL(44)', 'XL(42)', 'XL(46)', 'XL(40)', 'XL(48)', 'XL(38)'],
    "XXL": ["XXL", "XXL-L", "XXL-S", "XXL-M", "XXL-XL", "XXL-XXL", "XXL-XXXL", 'XXL(46)', 'XXL(48)', 'XXL(44)'],
}

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
for product in combined_data:
    # Normaliza tallas
    normalized_sizes = []
    for size in product["sizes"]:
        # Busca la talla normalizada correspondiente al size actual
        found = False
        for normalized_size, size_variants in sizes_dict.items():
            if size in size_variants:
                normalized_sizes.append(normalized_size)
                found = True
                break
        if not found:
            # Si no se ha encontrado una talla normalizada para el size actual,
            # se añade el size al array de tallas normal
            normalized_sizes.append(size)
    product["sizes"] = normalized_sizes

    # Normalizamos los precios para poder realizar busqueda con whoosh de rango
    price_discount = product["price_discount"]
    price_original = product["price_original"]

    #     "price_discount": "unknown" replace to "price_discount": 0.0
    if price_discount == "unknown":
        price_discount = "0.0"

    # Elimina el símbolo del euro de price_discount y price_original
    product["price_discount"] = float(
        price_discount.replace("€", "").replace(",", "."))
    product["price_original"] = float(
        price_original.replace("€", "").replace(",", "."))
    # Añade la propiedad currency y asigna a esta propiedad el valor "eur"
    product["currency"] = "eur"

# Escribimos la estructura de datos combinada a un nuevo archivo .json
with open(SAVE_FILE_PATH, "w") as f:
    json.dump(combined_data, f, indent=4)
