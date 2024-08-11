from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
 AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email,password, is_staff, is_superuser, is_active, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email = email,
                            is_staff = is_staff,
                            is_superuser = is_superuser,
                            is_active = is_active,
                            last_login = now,
                            date_joined = now,
                            **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, False, False, False, **extra_fields)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, True, **extra_fields)
        return user
    
class User(AbstractBaseUser,PermissionsMixin):
    """My own custom user class"""
    email = models.EmailField(max_length=255, unique=True, db_index=True,
                                verbose_name=_('email address'))
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def get_full_name(self):
        """Return the email."""
        return self.email
    
    def get_short_name(self):
        """Return the email."""
        return self.email
    
    
    
class Localisation(models.Model):
    localisation = models.CharField(max_length=100)
    prix_livraison = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = _('Localisation')
        verbose_name_plural = _('Localisations')
    
    def __str__(self):
        return str(self.localisation)
    
    

class Profile(models.Model):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = [
        (GENDER_MALE, _("Homme")),
        (GENDER_FEMALE, _("Femme")),
    ]
    
    COUNTRY = 'CI'
    COUNTRY_CHOICES = [
        (COUNTRY, _("Côte d'ivoire")),
    ]
    email_user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="user")
    nom = models.CharField(max_length=100, blank=True, default="", null=True)
    prenom = models.CharField(max_length=150, blank=True, default="", null=True)
    sexe = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True, default="", null=True)
    contact = models.CharField(max_length=10, blank=True, default="", null=True)
    ville = models.CharField(max_length=200, blank=True, default="", null=True)
    country = models.CharField(max_length=255, choices=COUNTRY_CHOICES, editable=False, default="CI")
    
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        
    def __str__(self):
        return str(self.email_user)