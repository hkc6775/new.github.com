from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.dashboard, name="accueil"),
    path('panier/', views.monPanier, name="panier"),
    path('produit/<str:category>/<str:id>', views.mesAchats, name="produit"),
]