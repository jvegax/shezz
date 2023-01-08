from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from shezz.search import combinated_search
from shezz.models import Product
from shezz.utils import is_superuser, loadDict
from shezz.forms import ProductForm, ProductRecommendationForm, SigninForm, SignupForm
from shezz.recommendations import sim_distance, topMatches, transformPrefs
import json
import shelve

PRODUCTS_DATA_PATH = 'data/all-products.json'


def home(request):
    if request.user.is_authenticated:
        form = ProductForm()
        return render(request, "home.html", {'form': form})
    else:
        return render(request, "welcome.html")

def signout(request):
    logout(request)
    return render(request, "welcome.html")
    

def signin(request):
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        signin_form = SigninForm(request.POST)
        # Validar la información del formulario
        if signin_form.is_valid():
            # Obtener la información del formulario limpia
            username = signin_form.cleaned_data['username']
            password = signin_form.cleaned_data['password']
            # Verificar las credenciales del usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Iniciar sesión
                login(request, user)
                # Redirigir al usuario a la página de inicio
                form = ProductForm()
                return render(request, 'home.html', {'form': form})
            else:
                # Redirigir al usuario al formulario de inicio de sesión
                return render(request, 'welcome.html', {'signin_form': signin_form, 'error': 'Usuario o contraseña incorrectos'})
    else:
        # Mostrar el formulario de inicio de sesión
        signin_form = SigninForm()
        return render(request, 'welcome.html', {'signin_form': signin_form})


def signup(request):
    if request.method == 'POST':
        # Obtener los datos del formulario de registro
        signup_form = SignupForm(request.POST)
        # Validar la información del formulario
        if signup_form.is_valid():
            # Obtener la información del formulario limpia
            username = signup_form.cleaned_data['username']
            password = signup_form.cleaned_data['password']
            email = signup_form.cleaned_data['email']
            first_name = signup_form.cleaned_data['first_name']
            last_name = signup_form.cleaned_data['last_name']
            # Crear un nuevo usuario
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            # Iniciar sesión
            login(request, user)
            # Redirigir al usuario a la página de inicio
            form = ProductForm()
            return render(request, 'home.html', {'form': form})
    else:
        # Mostrar el formulario de registro
        signup_form = SignupForm()
        return render(request, 'welcome.html', {'signup_form': signup_form})


@login_required
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

@user_passes_test(is_superuser)
def webmaster(request):
    return render(request, "webmaster.html")

@user_passes_test(is_superuser)
def populatedb(request):
    if request.method == "POST":
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
    else:
        return render(request, "webmaster.html", {"message": "No se ha poblado la base de datos"})

@user_passes_test(is_superuser)
def loadrs(request):
    if request.method == "POST":
        loadDict()
        return render(request, "webmaster.html", {"message": "Se ha cargado correctamente el diccionario de preferencias"})
    else:
        return render(request, "webmaster.html", {"message": "No se ha cargado el diccionario de preferencias"})

@login_required
def productos_similares(request):
    if request.method == 'POST':
        producto = None
        items = None
        formulario = ProductRecommendationForm(request.POST)

        if formulario.is_valid():
            idProducto = formulario.cleaned_data['idProducto']
            producto = get_object_or_404(Product, pk=idProducto)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()

            # Calcula los productos más similares al producto con ID idProducto
            parecidos = topMatches(Prefs, int(
                idProducto), n=3, similarity=sim_distance)
            productos = []
            similaridad = []
            for re in parecidos:
                productos.append(Product.objects.get(pk=re[1]))
                similaridad.append(re[0])
            items = zip(productos, similaridad)

        return render(request, 'productos_similares.html', {'form': formulario, 'producto': producto, 'items': items})
    else:
        formulario = ProductRecommendationForm()
        return render(request, 'productos_similares.html', {'form': formulario})
