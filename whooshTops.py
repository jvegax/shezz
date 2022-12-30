# Descripcion: genera el indice de busqueda de whoosh para los items de shein
from whoosh.fields import FieldType, Schema, TEXT, ID, STORED
from whoosh.analysis import StandardAnalyzer
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
import json

# Creamos un esquema para nuestros documentos
def create_shein_schema():
    # Creamos un nuevo tipo de campo llamado 'NAME'
    NAME = FieldType(format=TEXT, stored=True, analyzer=StandardAnalyzer())
    
    # Creamos un nuevo tipo de campo llamado 'ID'
    ID_TYPE = FieldType(format=ID , stored=True, analyzer=StandardAnalyzer())

    # Creamos un nuevo tipo de campo llamado 'STORED'
    STORED_TYPE = FieldType(format=STORED, stored=True, analyzer=StandardAnalyzer())

    # Creamos un esquema para nuestros documentos utilizando los tipos de campo que acabamos de crear
    schema = Schema(
        name=NAME(name="name"),
        sku = STORED_TYPE(name="sku"),
        price_discount=STORED_TYPE(name="price_discount"),
        price_original=STORED_TYPE(name="price_original"),
        category=STORED_TYPE(name="category"),
        rating=STORED_TYPE(name="rating"),
        product_link=STORED_TYPE(name="product_link"),
        sizes=STORED_TYPE(name="sizes"),
        images=STORED_TYPE(name="images")
    )

    # Creamos un índice en un directorio llamado "shein_index"
    ix = create_in("shein_index", schema)

    # Añadimos cada objeto como un documento al índice
    writer = ix.writer()

    with open("tops-mocked.json", "r") as tops_file:
        obj_list = json.load(tops_file)
        for obj in obj_list:
            # Creamos un objeto Field para cada campo del objeto
            sku_field = ID_TYPE(name="sku", value=obj['sku'])
            name_field = NAME(name="name", value=obj['name'])
            price_discount_field = STORED_TYPE(name="price_discount", value=obj['price_discount'])
            price_original_field = STORED_TYPE(name="price_original", value=obj['price_original'])
            category_field = STORED_TYPE(name="category", value=obj['category'])
            rating_field = STORED_TYPE(name="rating", value=obj['rating'])
            product_link_field = STORED_TYPE(name="product_link", value=obj['product_link'])
            sizes_field = STORED_TYPE(name="sizes", value=obj['sizes'])
            images_field = STORED_TYPE(name="images", value=obj['images'])
            
             # Añadimos los objetos Field al índice
            writer.add_field(sku_field)
            writer.add_field(name_field)
            writer.add_field(price_discount_field)
            writer.add_field(price_original_field)
            writer.add_field(category_field)
            writer.add_field(rating_field)
            writer.add_field(product_link_field)
            writer.add_field(sizes_field)
            writer.add_field(images_field)
        writer.commit()

def search_shenin_index(query):
    # Abrimos el índice que acabamos de crear
    shein_index = open_dir("shein_index")

    # Creamos un parseador de consultas para buscar por el campo 'name'
    query_parser = QueryParser("name", schema=shein_index.schema)

    # Creamos la consulta a partir de la cadena de texto que nos pasan `query`
    query_res = query_parser.parse(query)

    # Ejecutamos la búsqueda y obtenemos los resultados
    with shein_index.searcher() as searcher:
        results = searcher.search(query_res)
        for result in results:
            print(result)

create_shein_schema()