from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Profile, Localisation


class UserAdmin(BaseUserAdmin):
    list_display = ('email','is_staff','is_superuser', 'is_active')
    list_filter = ('is_staff',)
    fieldsets = ((None,{'fields':('email','password')}), ('Permissions',{'fields':('is_staff',)}),)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1','password2')}),)
    search_fields =('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Localisation)
admin.site.register(Profile)  