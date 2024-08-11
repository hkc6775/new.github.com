from .models import Profile, User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profil(sender, instance, created,**kwargs):
    if created:
        user_profil = Profile(email_user=instance)
        user_profil.save()
        
@receiver(pre_delete, sender=Profile)
def delete_user_profil(sender, instance, *args, **kwargs):
    pass