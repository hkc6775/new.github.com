from django.urls import path
from . import views

app_name = "commandes"

urlpatterns = [
    path('commandes', views.commandes_pages, name="show_commands"),
    path('deleted/<int:id>', views.deleteCommand, name="supprimer_commande"),
]