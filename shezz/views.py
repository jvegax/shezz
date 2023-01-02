from django.shortcuts import render
from .forms import ProductForm
from .search import combinated_search
# Create your views here.


def home(request):
    form = ProductForm()
    return render(request, "home.html", {"form": form})


def resultados(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            palabras_clave = form.cleaned_data["palabras_clave"]
            talla = form.cleaned_data["talla"]
            precio_desde = form.cleaned_data["precio_desde"]
            precio_hasta = form.cleaned_data["precio_hasta"]
            results = combinated_search(palabras_clave, talla, precio_desde, precio_hasta)
            return render(request, "resultados.html", {"results": results, "matches": len(results)})
        else:
            print("❌ Formulario no válido")
    else:
        return render(request, "resultados.html", {"results": None, "matches": 0})
            
