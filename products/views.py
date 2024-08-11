from django.shortcuts import render, redirect, HttpResponse
from forms.models import User, Profile, Localisation
from products.models import Poid, Produit, Categorie
from commandes.models import Commande
from forms.function import traitementEmail, traitementTel
import random
# Create your views here.
def dashboard(request):
    try:
        request.user is not None
        user = User.objects.get(pk=request.user.id)
        if user is not None:
            profil_user = Profile.objects.get(email_user=user)
            product = Produit.objects.all()
            return render(request, 'pages/products/index.html',
                            {
                            'userInfo':profil_user,
                            'product':product,
                            })
    except Exception:
        product = Produit.objects.all()
        return render(request, 'pages/products/index.html', {
            'product':product,
        })

def mesAchats(request, category, id):
    try:
        request.user is not None
        cat = Categorie.objects.get(categorie=category)
        product =  Produit.objects.get(pk=id, categorie=cat.id)
        poid = Poid.objects.filter(categorie=cat.id)
        commune = Localisation.objects.all()
        user = User.objects.get(pk=request.user.id)
        if user is not None:
            profil_user = Profile.objects.get(email_user=user)
            if request.method == "POST":
                prod = request.POST['prodName']
                prix = request.POST['poids']
                qts = request.POST['qts']
                username = request.POST['username']
                communes = request.POST['commune']
                phone = request.POST['contact']
                total = request.POST.get('Total')
                
                print(prod + "pd", prix + "px", qts + "pi", qts + "qts", username, communes, phone, total)
                    
                if prod != "" and prix != "" and qts != "" and username != "" and communes != "" and phone != "" and total != "":
                    if traitementEmail(username) == True:
                        if traitementTel(phone) == True:
                            form = Commande()
                            form.user_id = request.user.id
                            form.prodName = prod
                            form.prodPrix = prix
                            form.qts = qts
                            form.userName = username
                            form.commune = communes
                            form.tel = phone
                            form.total = total
                            form.ref = random.randint(10000000000, 99999999999)
                            form.save()
                                
                            return render(request, 'pages/products/commande_page.html',
                            {
                                'userInfo':profil_user,
                                'commune':commune,
                                'Poids':poid,
                                'product':product,
                                'succes': 'Succès ! Votre commande a été enregistré.',
                            })
                        else:
                            return render(request, 'pages/products/commande_page.html',
                            {
                                'userInfo':profil_user,
                                'commune':commune,
                                'Poids':poid,
                                'product':product,
                                'error': 'Erreur ! Contact non autorisé.',
                            })
                    else:
                        return render(request, 'pages/products/commande_page.html',
                        {
                            'userInfo':profil_user,
                            'commune':commune,
                            'Poids':poid,
                            'product':product,
                            'error': 'Erreur ! Caractère non autorisé.',
                        })
                else:
                    return render(request, 'pages/products/commande_page.html',
                        {
                            'userInfo':profil_user,
                            'commune':commune,
                            'Poids':poid,
                            'product':product,
                            'error': 'Erreur ! Veuillez repondre aux questions du formulaire aaa',
                        })
                    
            return render(request, 'pages/products/commande_page.html',
                    {
                        'userInfo':profil_user,
                        'commune':commune,
                        'Poids':poid,
                        'product':product,
                    })       
    except Exception as e:
        try:
            cat = Categorie.objects.get(categorie=category)
            product =  Produit.objects.get(pk=id, categorie=cat.id)
            poid = Poid.objects.filter(categorie=cat.id)
            commune = Localisation.objects.all()
            if request.method == "POST":
                form = Commande()
                prod = request.POST['prodName']
                prix = request.POST['poids']
                qts = request.POST['qts']
                username = request.POST['username']
                communes = request.POST['commune']
                phone = request.POST['contact']
                total = request.POST.get('Total')
                
                if prod != "" and prix != "" and qts != "" and username != "" and communes != "" and phone != "" and total != "":
                    if traitementEmail(username) == True:
                        if traitementTel(phone) == True:
                            form.prodName = prod
                            form.prodPrix = prix
                            form.qts = qts
                            form.userName = username
                            form.commune = communes
                            form.tel = phone
                            form.total = total
                            form.ref = random.randint(10000000000, 99999999999) 
                            form.save()
                            
                            return render(request, 'pages/products/commande_page.html',
                            {
                                'commune':commune,
                                'Poids':poid,
                                'product':product,
                                'succes': f"Succès ! Votre commande a été enregistré. La Ref:{form.ref}, veuillez l'enregistrer pour la vérification du status de la commande !",
                            })
                        else:
                            return render(request, 'pages/products/commande_page.html',
                            {
                                'commune':commune,
                                'Poids':poid,
                                'product':product,
                                'error': 'Erreur ! Contact non autorisé.',
                            })
                    else:
                        return render(request, 'pages/products/commande_page.html',
                        {
                            'commune':commune,
                            'Poids':poid,
                            'product':product,
                            'error': 'Erreur ! Caractère non autorisé.',
                        })
                else:
                    return render(request, 'pages/products/commande_page.html',
                        {
                            'commune':commune,
                            'Poids':poid,
                            'product':product,
                            'error': 'Erreur ! Veuillez repondre aux questions du formulaire',
                        })
                    
            return render(request, 'pages/products/commande_page.html',
                                {
                                    'commune':commune,
                                    'Poids':poid,
                                    'product':product,
                                })
        except Exception as e:
            return HttpResponse(e)
        
        
def monPanier(request):
    try:
        if request.user is not None:
            user = User.objects.get(pk=request.user.id)
            if user is not None:
                commune = Localisation.objects.all()
                profil_user = Profile.objects.get(email_user=user)
                if request.method == "POST":
                    cmmd = request.POST.get('commandes')
                    communes = request.POST.get('commune')
                    tel = request.POST.get('contact')
                    username = request.POST.get('username')
                    total = request.POST.get('sendTotal')
                    
                    if cmmd != "" and communes != "" and tel != "" and username != "" and total != "":
                        if traitementEmail(username) == True:
                            if traitementTel(tel) == True:
                                form = Commande()
                                form.user_id = request.user.id
                                form.prodName = cmmd
                                form.prodPrix = "price is multiple"
                                form.qts = "qts is multiple"
                                form.userName = username
                                form.commune = communes
                                form.tel = tel
                                form.total = total
                                form.ref = random.randint(10000000000, 99999999999) 
                                form.save()
                                
                                return render(request, 'pages/products/panier.html',
                                {
                                    'userInfo':profil_user,
                                    'commune':commune,
                                    'succes': f"Succès ! Votre commande a été enregistré. La Ref:{form.ref}, veuillez l'enregistrer pour la vérification du status de la commande !",
                                })
                            else:
                                return render(request, 'pages/products/panier.html',
                                {
                                    'userInfo':profil_user,
                                    'commune':commune,
                                    'error': 'Erreur ! Contact non autorisé.',
                                })
                        else:
                            return render(request, 'pages/products/panier.html',
                                {
                                    'userInfo':profil_user,
                                    'commune':commune,
                                    'error': 'Erreur ! Caractère non autorisé.',
                                })
                    else:
                        return render(request, 'pages/products/panier.html',
                            {
                                'userInfo':profil_user,
                                'commune':commune,
                                'error':'Erreur ! Veuillez repondre aux questions du formulaire.'
                            })
                return render(request, 'pages/products/panier.html',
                              {
                                  'userInfo':profil_user,
                                  'commune':commune,
                                  })
    except Exception as e:
        try:
            commune = Localisation.objects.all()
            if request.method == "POST":
                cmmd = request.POST.get('commandes')
                communes = request.POST.get('commune')
                tel = request.POST.get('contact')
                username = request.POST.get('username')
                total = request.POST.get('sendTotal')
                
                print(total)
                
                if cmmd != "" and communes != "" and tel != "" and username != "" and total != "":
                    if traitementEmail(username) == True:
                        if traitementTel(tel) == True:
                            form = Commande()
                            form.prodName = cmmd
                            form.prodPrix = "price is multiple"
                            form.qts = "qts is multiple"
                            form.userName = username
                            form.commune = communes
                            form.tel = tel
                            form.total = total
                            form.ref = random.randint(10000000000, 99999999999) 
                                    
                            form.save()
                            
                            return render(request, 'pages/products/panier.html',
                            {
                                'commune':commune,
                                'succes': f"Succès ! Votre commande a été enregistré. La Ref:{form.ref}, veuillez l'enregistrer pour la vérification du status de la commande !",
                            })
                        else:
                            return render(request, 'pages/products/panier.html',
                            {
                                'commune':commune,
                                'error': 'Erreur ! Contact non autorisé.',
                            })
                    else:
                        return render(request, 'pages/products/panier.html',
                        {
                            'commune':commune,
                            'error': 'Erreur ! Caractère non autorisé.',
                        })
                else:
                    return render(request, 'pages/products/panier.html',
                        {
                            'commune':commune,
                            'error':'Erreur ! Veuillez repondre aux questions du formulaire.'
                        })
            return render(request, 'pages/products/panier.html',
                            {
                                'commune':commune,
                            })
        except Exception as e:
            return HttpResponse(e)