# Descripcion: Este script combina los datos de dos archivos .json en uno solo

import json

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

# Escribimos la estructura de datos combinada a un nuevo archivo .json
with open(SAVE_FILE_PATH, "w") as f:
    json.dump(combined_data, f, indent=4)
