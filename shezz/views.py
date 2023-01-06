from django.shortcuts import render
from .forms import ProductForm
from shezz.models import Product
from .search import combinated_search
from django.contrib.auth.decorators import login_required, user_passes_test
import json

PRODUCTS_DATA_PATH = '/Users/jvegax/projects/python/shezz-env/shezz-repo/data/all-products.json'


def is_superuser(user):
    return user.is_superuser


def home(request):
    form = ProductForm()
    return render(request, "home.html", {"form": form})

# @login_required


def resultados(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            palabras_clave = form.cleaned_data["palabras_clave"]
            talla = form.cleaned_data["talla"]
            precio_desde = form.cleaned_data["precio_desde"]
            precio_hasta = form.cleaned_data["precio_hasta"]
            results, num_matches = combinated_search(
                palabras_clave, talla, precio_desde, precio_hasta)
            return render(request, "resultados.html", {"results": results, "matches": num_matches})
        else:
            print("❌ Formulario no válido")
    else:
        return render(request, "resultados.html", {"results": None, "matches": 0})

# @user_passes_test(is_superuser)


def webmaster(request):
    return render(request, "webmaster.html")

# @user_passes_test(is_superuser)


def populatedb(request):
    with open(PRODUCTS_DATA_PATH, 'r') as f:
        products_data = json.load(f)

    for product_data in products_data:
        product = Product(
            sku=product_data['sku'],
            name=product_data['name'],
            price_discount=product_data['price_discount'],
            price_original=product_data['price_original'],
            category=product_data['category'],
            rating=product_data['rating'],
            product_link=product_data['product_link'],
            sizes=product_data['sizes'],
            images=product_data['images'],
            currency=product_data['currency']
        )
        # Guarda la instancia en la base de datos
        product.save()

    num_products = Product.objects.count()
    return render(request, "webmaster.html", {"message": f"Se ha poblado la base de datos con {num_products} productos"})


# @user_passes_test(is_superuser)
def loadrs(request):
    pass
