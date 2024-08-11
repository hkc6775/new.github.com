from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Categorie(models.Model):
    categorie = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = _('Categorie')
        verbose_name_plural = _('Categories')
        
    def __str__(self):
        return str(self.categorie)    
    
class Poid(models.Model):
    poids = models.CharField(max_length=100)
    prix_poids = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _('Poid')
        verbose_name_plural = _('Poids')
    
    def __str__(self):
        return str(self.poids)
    
    
class Produit(models.Model):
    name = models.CharField(max_length=255)
    images_one = models.ImageField(upload_to='images/', max_length=100)
    images_to = models.ImageField(upload_to='images/', max_length=100)
    images_tree = models.ImageField(upload_to='images/', max_length=100)
    images_four = models.ImageField(upload_to='images/', max_length=100)
    images_five = models.ImageField(upload_to='images/', max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Produit')
        verbose_name_plural = _('Produits')
    
    def __str__(self):
        return str(self.name)
    