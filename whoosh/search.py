# Descripcion: Este scritp contiene las funciones para busqueda sobre el indice de whoosh
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import NumericRange
import sys

ARGS = sys.argv
SHEZZ_INDEX_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/whoosh/Index'


def search_by_name(query):
    shezz_index = open_dir(SHEZZ_INDEX_PATH)
    query_parser = QueryParser("name", schema=shezz_index.schema)
    query_res = query_parser.parse(query)

    with shezz_index.searcher() as searcher:
        results = searcher.search(query_res)
        print("✅ Found {} results.".format(len(results)))


def search_by_price():
    # Abrimos el índice que acabamos de crear
    shezz_index = open_dir(SHEZZ_INDEX_PATH)
    # Crea una consulta de rango para buscar productos con precio entre 10 y 20 con whoosh version 2.7.4
    numeric_range_query = NumericRange("price_original", 14, 15)
    with shezz_index.searcher() as searcher:
        results = searcher.search(numeric_range_query)
        for result in results:
            print(result["product_link"])
        print("✅ Found {} results.".format(len(results)))
         
        
search_by_price()
