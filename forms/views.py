from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
#importing as such so that it doesn't create a confusion with our methods and django's default methods
from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, RegistrationForm, Profiles, Edition_mailForm, Edition_passwordForm
from .models import Profile, Localisation, User
from .email import Envoyer_page_html_par_mail
from django.contrib.sites.shortcuts import get_current_site
from .cryter_chaine import encoder, decoder
import random
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import (
 xframe_options_exempt, xframe_options_deny, xframe_options_sameorigin,
)
from .function import traitementEmail, traitementTel

@method_decorator(xframe_options_deny, name='dispatch')
def login(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(data = request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = django_authenticate(email=email, password=password)
                if user is not None:
                    if user.is_active:
                        django_login(request,user)
                        return redirect('products:accueil') #user is redirected to dashboard
                        
        else:
            form = AuthenticationForm()
        return render(request,'pages/login.html',{'form':form,})
    except Exception as e:
        form = AuthenticationForm()
        return render(request,'pages/login.html',{'form':form,})


@method_decorator(xframe_options_deny, name='dispatch')
def register(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(data = request.POST)
            if form.is_valid():
                domaine = get_current_site(request)
                email = request.POST['email']
                result = Envoyer_page_html_par_mail('Mail de vérification', 
                                                    'email_pages/confirm_mail.html',
                                                    request.POST['email'], encoder(email), domaine, email)
                if result:
                    user = form.save()
                    django_login(request,user)
                    succes = "Succès ! Votre compte a été créer. Un mail de confirmation vous a été envoyer."
                    form = AuthenticationForm()
                    return render(request, 'pages/login.html', {
                        'succes':succes,
                        'form':form,
                    })
                else:
                    form = RegistrationForm()
                    return render(request,'pages/logun.html',{'form':form,'error':'Erreur de traitement. Veuillez rééssayé !'})   
        else:
            form = RegistrationForm()
        return render(request,'pages/logun.html',{'form':form,})
    except Exception as e:
        form = RegistrationForm()
        return render(request,'pages/logun.html',{'form':form,})

@method_decorator(xframe_options_deny, name='dispatch')
def confirm_mail(request, user_mail):
    try:
        user_mail = decoder(str(user_mail))
        if user_mail:
            user = User.objects.get(email = user_mail)
            if user is not None:
                print(user.is_active)
                if user.is_active == False:
                    user.is_active = True
                    user.save()
                    form = AuthenticationForm()
                    print(user.is_active)
                    return render(request,'pages/login.html',{'form':form,'succes':'Vérification du mail réussi ! Veuillez à présent vous connectez.'})
                else:
                    form = RegistrationForm()
                    return render(request,'pages/logun.html',{'form':form,'succes':'Votre compte a été confirmer. Veuiller vous connectez !'})
            else:
                form = RegistrationForm()
                return render(request,'pages/logun.html',{'form':form,'error':'La vérification de votre mail a échoué !'})
        else:
            form = RegistrationForm()
            return render(request,'pages/logun.html',{'form':form,'error':'La vérification de votre mail a échoué !'})
    except Exception as e: 
        form = RegistrationForm()
        return render(request,'pages/logun.html',{'form':form,'error':'La vérification de votre mail a échoué !'})

def logout(request):
    django_logout(request)
    return redirect('products:accueil')


@method_decorator(xframe_options_deny, name='dispatch')
@login_required(login_url ="forms:login")
def infos_suplemented(request):
    try:
        if request.user.id is not None:
            user_profile = Profile.objects.get(email_user=request.user)
            if request.method == "POST":
                form = Profiles(request.POST)
                if form.is_valid:
                    if request.POST['nom'] != "" and request.POST['nom'] != user_profile.nom and traitementEmail(request.POST['nom']) == True:
                        user_profile.nom = request.POST['nom']
                        user_profile.save()
                        
                    if request.POST['prenom'] != "" and request.POST['prenom'] != user_profile.prenom and traitementEmail(request.POST['prenom']) == True:
                        user_profile.prenom = request.POST['prenom']
                        user_profile.save()
                        
                    if request.POST['sexe'] != "" and request.POST['sexe'] != user_profile.sexe:
                        user_profile.sexe = request.POST['sexe']
                        user_profile.save()
                        
                    if request.POST['contact'] != "" and request.POST['contact'] != user_profile.contact and traitementTel(request.POST['contact']) == True:
                        user_profile.contact = request.POST['contact']
                        user_profile.save()
                    
                    if request.POST['ville'] != "" and request.POST['ville'] != user_profile.ville:
                        user_profile.ville = request.POST['ville']
                        user_profile.save()      
                        print(request.user, user_profile.ville, request.POST['ville'])
                        
                else:
                    print('Erreur de traitement')
                
            else:
                form = Profiles(request.POST)
            return render(request, "pages/infos.html", {
                "form":form,
                'user':user_profile,
                'regions':Localisation.objects.all().order_by('id'),
                })
        logout(request)
        form = RegistrationForm()
        return render(request,'pages/login.html',{'form':form,})
    except Exception as e:
        logout(request)
        form = AuthenticationForm()
        return render(request,'pages/login.html',{'form':form,})


@method_decorator(xframe_options_deny, name='dispatch')
@login_required(login_url ="forms:login")
def edit_email(request):
    if request.user.id is not None:
        user = User.objects.get(email=request.user)
        if request.method == "POST":
            form = Edition_mailForm(request.POST)
            if form.is_valid():
                domaine = get_current_site(request)
                if request.POST['email'] != "":
                    try:
                        context = {
                            'ancien_mail':encoder(user.email),
                            'new_mail': encoder(request.POST['email']),
                        }
                        Envoyer_page_html_par_mail(
                            'Edition du mail',
                            'email_pages/edit_mail.html',
                            user.email,
                            context,
                            domaine,
                            user.email
                        )
                        user.is_active = False
                        user.save()
                        form = Edition_mailForm(request.POST)
                        return render(request, 'pages/edit_mail.html', {
                            'form':form,
                            'succes': f"Un mail de vérification vous a été envoyer à l'addresse {user.email}",
                            })
                    except Exception as e:
                        return render(request, 'pages/edit_mail.html', {
                            'form':form,
                            'error': f"Erreur ! Traitement échoué.",
                            }) 
        else:
            form = Edition_mailForm()
        return render(request, 'pages/edit_mail.html', {
            'form':form,
            'user':user,
            })
    else:
        return redirect('forms:login')
    
    
def is_me(request, ancien_mail, new_mail):
    try:
        ancien_mail = decoder(ancien_mail)
        print(ancien_mail)
        new_mail = decoder(new_mail)
        print(new_mail)
        domaine = get_current_site(request)
        
        if ancien_mail and new_mail:
            user = User.objects.get(email=ancien_mail)
            if user is not None:
                try:
                    user.email = new_mail
                    user.is_active = False
                    user.save()
                    
                    result = Envoyer_page_html_par_mail(
                        'Vérification du mail',
                        'email_pages/verify_mail.html',
                        new_mail,
                        encoder(new_mail),
                        domaine,
                        new_mail
                    )
                    if result:
                        django_logout(request)
                        form = AuthenticationForm()
                        return render(request, 'pages/login.html', {
                            'form':form,
                            'succes': f"Succès ! Modification éfféctuée. Un mail de vérification vous a été énvoyer {new_mail}",
                        })
                    else:
                        django_logout(request)
                        form = AuthenticationForm()
                        return render(request, 'pages/login.html', {
                            'form':form,
                            'error': f"Erreur ! Traitement échoué. Veuillez réessayer ! mail nom envoyer",
                        })
                except Exception as e:
                    django_logout(request)
                    form = AuthenticationForm()
                    return render(request, 'pages/login.html', {
                        'form':form,
                        'error': f"Erreur ! Traitement échoué (mail existe déjà ou erreur de traitement). Veuillez réessayer !",
                    })
            else:
                django_logout(request)
                form = AuthenticationForm()
                return render(request, 'pages/login.html', {
                    'form':form,
                    'error': f"Erreur ! Traitement échoué. Veuillez réessayer ! aaaa",
                })
        else:
            django_logout(request)
            form = AuthenticationForm()
            return render(request, 'pages/login.html', {
                    'form':form,
                    'error': f"Erreur ! Traitement échoué. Veuillez réessayer !",
                })
    except Exception as e:
        django_logout(request)
        form = AuthenticationForm()
        return render(request, 'pages/login.html', {
                'form':form,
                'error': f"Erreur ! Traitement échoué. Veuillez réessayer ! {e}",
            })

def is_not_me(request, ancien_mail):
    try:
        ancien_mail = decoder(str(ancien_mail))
        if ancien_mail:
            user = User.objects.get(email=ancien_mail)
            if user is not None:
                user.is_active = True
                user.save()
                django_logout(request)
                form = AuthenticationForm()
                return render(request, 'pages/login.html', {
                    'form':form,
                    'succes': f"Succès ! Vérification du mail réussi.",
                })
            else:
                django_logout(request)
                form = AuthenticationForm()
                return render(request, 'pages/login.html', {
                    'form':form,
                    'error': f"Erreur ! Traitement échoué. Veuillez réessayer !",
                })
    except Exception as e:
        django_logout(request)
        form = AuthenticationForm()
        return render(request, 'pages/login.html', {
                'form':form,
                'error': f"Erreur ! Traitement échoué. Veuillez réessayer !",
            })

@method_decorator(xframe_options_deny, name='dispatch')
@login_required(login_url ="forms:login")
def edit_password(request):
    if request.user.id is not None:
        if request.method == "POST":
            form = Edition_passwordForm(request.POST)
            if form.is_valid():
                try:
                    mdp = request.POST['password']
                    newmdp = request.POST['newpassword']
                    if mdp and newmdp:
                        user = django_authenticate(email=request.user, password=mdp)
                        if user is not None:
                            user.set_password(newmdp)
                            user.save()
                            return render(request, 'pages/password_edit.html',{
                                'form':form,
                                'succes':"Succes ! Modification du mot de passe réussi."
                                })
                        else:
                            form = Edition_passwordForm(request.POST)
                            return render(request, 'pages/password_edit.html',{
                                'form':form,
                                'error':f"Erreur ! Traitement échoué. Veuillez Réessayer !"
                                })
                    else:
                        form = Edition_passwordForm(request.POST)
                        return render(request, 'pages/password_edit.html',{
                            'form':form,
                            'error':"Erreur ! Veuillez entrée tous les champs !"
                            })
                except Exception as e:
                    form = Edition_passwordForm()
                    return render(request, 'pages/password_edit.html',{
                        'form':form,
                        'error':f"Erreur ! Traitement échoué. Veuillez Réessayer !"
                        })
        else:
            form = Edition_passwordForm()
        return render(request, 'pages/password_edit.html',{'form':form})
    else:
        return redirect('forms:login')
    

@method_decorator(xframe_options_deny, name='dispatch')
def recup_compte(request):
    if request.method == "POST":
        form = Edition_mailForm(request.POST)
        if form.is_valid():
            if request.POST['email'] != "":
                try:
                    user = User.objects.get(email=request.POST['email'])
                    if user.is_active == True:
                        domaine = get_current_site(request)
                        code = random.randint(1111, 9999)
                        context = {
                            'code':code,
                            'codesh':code
                        }
                        result = Envoyer_page_html_par_mail(
                                'Récupération de compte',
                                'email_pages/recup.html',
                                request.POST['email'],
                                encoder(request.POST['email']),
                                domaine,
                                context
                            )
                        if result:
                            return render(request, 'pages/recup.html', {
                            'form':form,
                            'succes':f"Succès ! Un mail vous a été envoyer à l'adresse {request.POST['email']}."
                            })
                    else:
                        return render(request, 'pages/recup.html', {
                        'form':form,
                        'error':'Erreur ! Veuillez confirmer votre compte.'
                        })
                except Exception as e:
                    return render(request, 'pages/recup.html', {
                    'form':form,
                    'error':f'Erreur ! Mail introuvable.{e}'
                    })
        else:
            return render(request, 'pages/recup.html', {
                'form':form,
                'error':'Erreur ! Traitement a échoué.'
                })
            
    form = Edition_mailForm()
    return render(request, 'pages/recup.html', {'form':form})


def change_mdp(request, email, mdp):
    try:
        email = decoder(email)
        
        if email and mdp:
            try:
                user = User.objects.get(email=email)
                if user is not None:
                    user.set_password(mdp)
                    user.save()
                    form = AuthenticationForm()
                    return render(request, 'pages/login.html', {
                        'form':form,
                        'succes':'Succès ! Mot de passe modifier.'
                    })
                else:
                    return render(request, 'pages/recup.html', {
                    'form':form,
                    'error':'Erreur ! Traitement a échoué.'
                    })
            except Exception as e:
                return render(request, 'pages/recup.html', {
                    'form':form,
                    'error':'Erreur ! Traitement a échoué.'
                    })
        else:
            form = Edition_mailForm()
            return render(request, 'pages/recup.html', {
                    'form':form,
                    'error':'Erreur ! Traitement a échoué.'
                    })
    except Exception as e:
        form = Edition_mailForm()
        return render(request, 'pages/recup.html', {
                'form':form,
                'error':'Erreur ! Traitement a échoué.'
                })
        
def page404(request, exception):
    return render(request, "error_page/404.html")