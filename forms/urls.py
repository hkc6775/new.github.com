from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('deconnected/', views.logout, name="deconnected"),
    path('infos_suplemented/', views.infos_suplemented, name="infos_suplemented"),
    path('verification_du_mail/<str:user_mail>/', views.confirm_mail),
    path('edit_mail/', views.edit_email, name='mail_edition'),
    path('edit_password/', views.edit_password, name='password_edition'),
    path('yes_is_me/<str:ancien_mail>/<str:new_mail>/', views.is_me),
    path('no_is_not_me/<str:ancien_mail>/', views.is_not_me),
    path('recuperation/', views.recup_compte, name='recup'),
    path('changePassword/<str:email>/<str:mdp>/', views.change_mdp),
]