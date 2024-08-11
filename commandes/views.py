from django.shortcuts import render
from forms.models import User
from commandes.models import Commande
from datetime import datetime
from forms.function import traitementEmail
from django.http import HttpResponse
# Create your views here.
def commandes_pages(request):
    try:
        request.user is not None
        user = User.objects.get(id=request.user.id)
        if user is not None:
            cmmd = Commande.objects.filter(user_id=user.id).order_by('-id')
            cmmdes = Commande.objects.filter(user_id=user.id).order_by('-id')
            if request.method == "POST":
                ref = request.POST.get('dates')
                if ref is not None:
                    cmmds = Commande.objects.filter(ref=ref).order_by('-id')
                    if len(cmmd) != 0:
                        context = {
                            'commandes':cmmds,
                            'cmmd':cmmdes,
                        }
                        return render(request, 'pages/commandes/commandes.html', {
                            'ctx':context,
                        })
                    else:
                        from django.shortcuts import redirect
                        return redirect('commandes:show_commands')
            if len(cmmd) != 0:
                context = {
                    'commandes':cmmd,
                    'cmmd':cmmdes,
                }
                return render(request, 'pages/commandes/commandes.html', {
                    'ctx':context,
                })
            else:
                return render(request, 'pages/commandes/commandes.html')
    except Exception as e:
        if request.method == "POST":
            search = request.POST.get('search')
            if traitementEmail(search) == True:
                Command = Commande.objects.filter(ref=search).order_by('-ref')
                if len(Command) != 0:
                    context = {
                        'commandes':Command,
                    }
                    return render(request, 'pages/commandes/commandes.html', {'ctx':context})
        return render(request, 'pages/commandes/commandes.html')
    
    
    
def deleteCommand(request, id):
    try:
        id = int(id)
        commande = Commande.objects.get(id=id)
        commande.annuler = True
        commande.save()
        from django.shortcuts import redirect
        return redirect('commandes:show_commands')
    except Exception as e:
        return HttpResponse(e)