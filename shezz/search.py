# Descripcion: Este scritp contiene las funciones para busqueda sobre el indice de whoosh
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import NumericRange, Term, And
import sys

ARGS = sys.argv
SHEZZ_INDEX_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/whoosh/Index'


def normlize_name_length(name):
    if len(name) > 47:
        return name[:47] + "..."
    else:
        return name


def normalize_sizes_to_string(sizes):
    # ['S', 'M', 'L'] -> 'S, M, L'
    return ", ".join(sizes)


def search_by_name(query):
    shezz_index = open_dir(SHEZZ_INDEX_PATH)
    query_parser = QueryParser("name", schema=shezz_index.schema)
    query_res = query_parser.parse(query)

    with shezz_index.searcher() as searcher:
        results = searcher.search(query_res)
        print("✅ Found {} results.".format(len(results)))


def search_by_price_range():
    # Abrimos el índice que acabamos de crear
    shezz_index = open_dir(SHEZZ_INDEX_PATH)
    # Crea una consulta de rango para buscar productos con precio entre 10 y 20 con whoosh version 2.7.4
    numeric_range_query = NumericRange("price_original", 12, 15)
    with shezz_index.searcher() as searcher:
        results = searcher.search(
            numeric_range_query, limit=20, sortedby="price_original")
        # obtener los 20 primeros resultados de la búsqueda y mostrarlos en pantalla
        print("✅ Found {} results.".format(len(results)))
        for result in results:
            print(result["name"], result["price_original"])


def search_by_size(query):
    shezz_index = open_dir(SHEZZ_INDEX_PATH)
    query_res = Term("sizes", query)

    with shezz_index.searcher() as searcher:
        # Realiza la búsqueda y muestra el número de resultados
        results = searcher.search(query_res, limit=20)
        for result in results:
            print(result["name"], result["sizes"])
        print("✅ Found {} results.".format(len(results)))


def combinated_search(name_query, size_query, min_price, max_price):
    matches = []
    num_matches = 0
    # Abrimos el índice Whoosh
    shezz_index = open_dir(SHEZZ_INDEX_PATH)

    # Creamos las consultas de búsqueda para cada campo
    name_query_parser = QueryParser("name", schema=shezz_index.schema)
    name_query_res = name_query_parser.parse(name_query)

    size_query_res = Term("sizes", size_query)

    price_range_query = NumericRange("price_original", min_price, max_price)

    # Creamos la consulta combinada utilizando la clase And
    combined_query = And([name_query_res, size_query_res, price_range_query])

    # Realizamos la búsqueda utilizando la consulta combinada
    with shezz_index.searcher() as searcher:
        results = searcher.search(
            combined_query, limit=20, sortedby="price_original")
        num_matches = len(results)
        for result in results:
            new_match = {
                "name": normlize_name_length(result["name"]),
                "price_original": result["price_original"],
                "price_discount": result["price_discount"],
                "sizes": normalize_sizes_to_string(result["sizes"]),
                "product_link": result["product_link"],
                "images": result["images"],
                "rating": result["rating"],
            }
            matches.append(new_match)

    return matches, num_matches


# search_by_price_range()
# search_by_size(ARGS[1])
# combinated_search(ARGS[1], ARGS[2], int(ARGS[3]), int(ARGS[4]))
