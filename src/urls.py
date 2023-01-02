from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from shezz import views as shezz_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shezz_views.home, name='home'),
    path('resultados/', shezz_views.resultados, name='resultados')
]
urlpatterns += staticfiles_urlpatterns()
