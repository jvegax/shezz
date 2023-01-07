from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from shezz import views as shezz_views

urlpatterns = [
    path('', shezz_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signin/', shezz_views.signin, name='signin'),
    path('signup/', shezz_views.signup, name='signup'),
    path('logout/', shezz_views.signout, name='logout'),
    
    path('productos-similares/', shezz_views.productos_similares, name='productos_similares'),
    path('resultados/', shezz_views.resultados, name='resultados'),
    
    path('webmaster/', shezz_views.webmaster, name='webmaster'),
    path('webmaster/populatedb/', shezz_views.populatedb, name='populatedb'),
    path('webmaster/loadrs/', shezz_views.loadrs, name='loadrs'),
]
urlpatterns += staticfiles_urlpatterns()
