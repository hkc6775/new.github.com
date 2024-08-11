from django.contrib import admin
from .models import Poid, Categorie, Produit

# Register your models here.
admin.site.register(Poid)
admin.site.register(Categorie)
admin.site.register(Produit)