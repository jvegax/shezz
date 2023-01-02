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


def search_by_price(range_query):
    # Abrimos el índice que acabamos de crear
    shezz_index = open_dir(SHEZZ_INDEX_PATH)

    # Creamos una consulta de rango utilizando NumericRange
    lower_bound, upper_bound = range_query.split("-")
    query_res = NumericRange(
        'price_original', lower_bound, upper_bound, include_lower=True, include_upper=True)

    with shezz_index.searcher() as searcher:
        # Realizamos la búsqueda utilizando la consulta de rango
        results = searcher.search(query_res, limit=None)
        for result in results:
            print(result)
        print("✅ Found {} results.".format(len(results)))
        
search_by_price(ARGS[1])
