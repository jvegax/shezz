# Descripcion: genera el indice de busqueda de whoosh para los items de shein

from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.analysis import StandardAnalyzer
from whoosh.index import create_in, open_dir, Document
from whoosh.qparser import QueryParser
import json

# Creamos un esquema para nuestros documentos


def create_shein_schema():
    schema = Schema(
        sku=ID(stored=True),
        name=TEXT(stored=True, analyzer=StandardAnalyzer()),
        price_discount=STORED,
        price_original=STORED,
        category=STORED,
        rating=STORED,
        product_link=STORED,
        sizes=STORED,
        images=STORED
    )

    # Creamos un índice en un directorio llamado "indexdir"
    ix = create_in("shein_index", schema)

    # Añadimos cada objeto como un documento al índice
    writer = ix.writer()

    with open("tops-mocked.json", "r") as tops_file:
        obj_list = json.load(tops_file)
        for obj in obj_list:
            doc = Document(
                sku=obj['sku'],
                name=obj['name'],
                price_discount=obj['price_discount'],
                price_original=obj['price_original'],
                category=obj['category'],
                rating=obj['rating'],
                product_link=obj['product_link'],
                sizes=obj['sizes'],
                images=obj['images']
            )
            writer.add_document(doc)
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
