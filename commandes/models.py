from django.db import models
import random
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from datetime import datetime
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Commande(models.Model):
    user_id = models.CharField(max_length=255, blank=True, null=True, default="no user")
    prodName = models.CharField(max_length=200000000)
    prodPrix = models.CharField(max_length=255)
    qts = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    tel = models.CharField(max_length=10)
    total = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    ref = models.CharField(max_length=255, blank=True)
    codeBar = models.ImageField(upload_to="codeBarCmmd/", blank=True)
    status = models.BooleanField(default=False)
    annuler = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Commande')
        verbose_name_plural = _('Commandes')
    
    def __str__(self):
        return self.userName
    
    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f'{random.randint(1000000000000, 9999999999999)}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.codeBar.save(f'barcode{datetime.now()}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)