from django.shortcuts import render
from .forms import ProductForm
from .search import combinated_search
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

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
    pass

# @user_passes_test(is_superuser)
def loadrs(request):
    pass
