from django.urls import path
from . import views

urlpatterns = [
    path('country-population/', views.country_population, name='country_population'),
    path('top-populated/', views.top_populated_countries, name='top_populated_countries')
]
