from shezz.recommendations import transformPrefs
from shezz.models import Product
import shelve

def is_superuser(user):
    return user.is_superuser

# Carga el diccionario Prefs en el archivo dataRS.dat para ser usado por el sistema de recomendación
def loadDict():
    Prefs = {}
    shelf = shelve.open("dataRS.dat")
    products = Product.objects.all()  # obtiene todos los productos
    for product in products:
        itemid = product.id
        rating = product.rating
        Prefs.setdefault(itemid, {})
        Prefs[itemid]['rating'] = rating
        Prefs[itemid]['price_original'] = product.price_original
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf.close()