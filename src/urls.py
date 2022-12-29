from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from shezz import views as shezz_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shezz_views.home, name='home'),
    path('scrapp/', shezz_views.scrapp, name='scrapp'),
]
urlpatterns += staticfiles_urlpatterns()
