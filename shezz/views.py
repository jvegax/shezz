from django.shortcuts import render
from .scraper import scrap_links_tops_shein

# Create your views here.


def home(request):
    return render(request, "base.html")


def scrapp(request):
    if request.method == 'POST':
        scrap_links_tops_shein()
    return render(request, "scrapp/scrapp.html")

