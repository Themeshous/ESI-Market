from cProfile import label
from django.db.models import Q
from multiprocessing import context
import django.contrib.sessions 
from django.forms.widgets import HiddenInput
from django.contrib.auth.hashers import make_password
from django.db.models.base import Model
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from suivi.models import Dossier, Op_Dos, Operateur, Utils, Lot
from suivi.models import Profile as P
from django.utils import timezone
import simple_history
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from datetime import date, time
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User,Group
from django.urls import reverse 
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from .forms import Control_initialForm, EvaluationForm, LancementForm, Op_DosForm, Precommande1Form, ProfileCreationForm, Suivi1Form, Suivi2Form, Suivi3Form, Suivi4Form, UtilsForm, FournisseurCreationForm, DepositaireForm, ClassementForm, Suivi_commandeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

import datetime
from datetime import datetime
from .filters import RequeteFilter
from .forms import UserForm, UserUpdateForm, ProfileUpdateForm
from django.forms import modelformset_factory
from django.forms import inlineformset_factory



def get_login(request):
    return render(request,'suivi/login.html')

def login_request(request):
    if request.user.is_authenticated:

        if request.user.profile.profil=="Administrateur":
            return redirect('Admin')
        else:
            if request.user.groups.filter(name="Comptable").exists():
                return redirect('Menu_Comptable')
            if request.user.groups.filter(name="Commande").exists():
                return redirect('Menu_Commande')
            if request.user.groups.filter(name="Budget").exists():
                return redirect('Menu_Budget')
            if request.user.groups.filter(name="Marche").exists():
                return redirect('Menu_Marche')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.profile.profil=="Administrateur":
                    return redirect('Admin')
                elif user.profile.profil =="Ordonnateur":
                    return redirect('Ordonnateur')
                else:
                    if user.groups.filter(name="Comptable").exists():
                        return redirect('Menu_Comptable')
                    if user.groups.filter(name="Commande").exists():
                        return redirect('Menu_Commande')
                    if user.groups.filter(name="Budget").exists():
                        return redirect('Menu_Budget')
                    if user.groups.filter(name="Marche").exists():
                        return redirect('Menu_Marche')
       
                messages.info(request, f"Vous etes connecté en tant que: {username}")
                
            else:
                messages.error(request, "Email ou mot de passe invalide.")
        else:
            messages.error(request, "Email ou mot de passe invalide.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "suivi/login.html",
                    context={"form":form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('reset')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def del_user(request, username):    
    u = User.objects.get(username = username)
    u.delete()
    messages.success(request, "L'utilisateur a été supprimé")
    context={}
    context["users"]=User.objects.all()
    return redirect('Liste_Profiles')

def Affich_Profile(request, user):
    return render (request, 'suivi/affich_profil.html')

def Profile(request, user):
    u=get_object_or_404(User,username=user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=u)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=u.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            u.save()
            messages.success(request, "Profil modifé avec succès")
            return redirect('Profile', user)
    else:
        u_form = UserUpdateForm(instance=u)
        p_form = ProfileUpdateForm(instance=u.profile)
        
    context = {
        'u' : user,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'suivi/profil.html', context)

   


def Contact (request):
    return render(request, 'suivi/contact.html')

def Admin(request):

    return render (request, 'suivi/admin.html')

def Ordonnateur(request):
    return render( request, 'suivi/ordonnateur.html')

def Modifier_Dates(request):
    return render(request, 'suivi/modifier_dates.html')


def Liste_Profiles(request):

    context={}
    context["users"]=User.objects.all().exclude(is_superuser=True)
    

    return render (request, 'suivi/liste_profiles.html',context)


def Historique(request):
    history=Dossier.history.all()
    return render(request, 'suivi/historique.html',{'history':history})

def Ajouter_User(request):
    u_form = UserForm(request.POST or None)  
    p_form = ProfileCreationForm(request.POST or None)
    
    forms={'u_form':u_form,'p_form':p_form}

    if u_form.is_valid() and p_form.is_valid():
        user = u_form.save()
        for value in u_form.cleaned_data['group']:
            group = Group.objects.get(name= value)
            group.user_set.add(user)
        
        user.save()
        profile = p_form.save(commit=False)
        profile.user = user
        profile.save()
          
        messages.success(request, "Création de l'utilisateur avec Succées")
    return render(request, 'suivi/add_user.html', forms)

def annee_commerciale(request):
    todays_date = date.today()
    a = Utils.objects.get(id=1)
    a.year = todays_date
    a.save()
    table_rows = Dossier.objects.all()
    for row in table_rows.values():
        Archive.objects.create(**row)
        table_rows.delete()

    return render(request, 'suivi/ordonnateur.html')
def modif_duree(request):
    u=get_object_or_404(Utils,id=1)
    if request.method == 'POST':
        form = UtilsForm(request.POST, instance=u)
        if form.is_valid():
            form.save()
            u.save()
            messages.success(request, "Les durée de traitement de données ont été modifés")
            return redirect('modif_duree')
    else:
        form = UtilsForm(instance=u)

        
    context = {
        'form': form,
    }
    return render(request, 'suivi/modif_duree.html', context)


def Comptable(request):
    data = Dossier.objects.all()
    liste=[]
    for q in data:
        if q.complement==None or q.recC==None:
            Dur="Non valide"
        else:
            delta=q.complement - q.recC
            Dur=str(delta.days)+" jours"
        liste.append({
            'Num' : q.num_dossier,
            'Rec' : q.recC,
            'Resp' : q.respC,
            'Decision' : q.decisionC,
            'Piece' : q.pieces,
            'Complement' : q.complement,
            'Paiements' : q.paiement,
            'Prolongation' : q.prolongation,
            'Observation' : q.observationsC,
            'Duree' : Dur,
            })
    return render(request, 'suivi/comptable.html',{'data':liste}) 
    
def Budget(request):
    data = Dossier.objects.all()
    liste=[]
    for q in data: 
        if q.transmissionB==None or q.recB==None:
            Dur="Non valide"
        else:
            delta=q.transmissionB - q.recB
            Dur=str(delta.days)+" jours"
        liste.append({
            'Num' : q.num_dossier,
            'Rec' : q.recB,
            'Resp' : q.respB,
            'Obs' : q.observationB,
            'Eng' : q.engagement,
            'Mot' : q.motifs,
            'Visa' : q.visa,
            'Trans' : q.transmissionB,
            'Dur' : Dur,
            'Prof' : q.mandatement,
        })
    return render(request, 'suivi/budget.html', {'data': liste})

def Commande(request):
    data = Dossier.objects.all()
    liste=[]
    for q in data:
        if q.transmission==None or q.recCo==None:
            Dur="Non valide"
        else:
            delta=q.transmission - q.recCo
            Dur=str(delta.days)+" jours"
        liste.append({
            'Num' : q.num_dossier,
            'Rec' : q.recCo,
            'Resp' : q.respCo, 
            'Dec': q.decisionCo,
            'Obs' : q.observation,
            'Prof' : q.proformaCo,
            'DateProf' : q.dproforma, 
            'Mon' : q.montant,
            'Bonc' : q.bonc,
            'Dbonc' : q.dbonc,
            'Prest' : q.prestation,
            'Def' : q.définitive,
            'Bonr' : q.bonr,
            'Trans' : q.transmission,
            'Dur' : Dur,

        })
    return render(request, 'suivi/commande.html', {'data' : liste})

def Marche(request):
    data = Dossier.objects.all()
    liste=[]
    for q in data: 
        if q.transmissionM==None or q.lancement==None:
            Dur="Non valide"
        else:
            delta=q.transmissionM - q.lancement
            Dur=str(delta.days)+" jours"
        liste.append({
            'Num' : q.num_dossier,          
            'Type' : q.type_dossier,
            'Obj' : q.objet,
            'Ouver' : q.ouverture,
            'Lanc' : q.lancement,
            'Fourn' : q.fournisseur,
            'Trans' : q.transmissionM,
            'Dec' : q.decisionM,
            'Conv' : q.convention,
            'Resp' : q.respM,
            'Dur' : Dur,
            'Obvs' : q.observationM,
        })
    return render(request, 'suivi/marche.html', {'data': liste})   





def Inserer_Commande(request):
    context={}
    nb=Dossier.objects.last()
    a = Utils.objects.get(id=1)
    today=date.today()
    form= CommandeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Insertion avec Succées")
        return redirect('Menu_Commande')
    context['form']=form
    context['nb']=nb
    context['today']=today
    context['a']=a
    return render(request, 'suivi/inserer_comm.html', context)

def Inserer_Marche(request):
    context={}
    nb=Dossier.objects.last()
    today=date.today()
    a = Utils.objects.get(id=1)
    form = MarcheForm(request.POST or None)
    if form.is_valid():

        form.save()
        messages.success(request, "Insertion avec Succées")
        return redirect('Menu_Marche')
    context['form']=form
    context['nb']=nb
    context['today']=today
    context['a']=a
    return render(request,'suivi/inserer_marche.html', context)

def Consulter_Dossier(request,id):
    dossier = get_object_or_404(Dossier, pk=id)
   
    if dossier.transmissionB==None or dossier.recB==None:
        dossier.dureeB='Durée non valide'
        dossier.save()
    else:
        delta = dossier.transmissionB - dossier.recB
        dossier.dureeB=str(delta.days)+" jours"
        dossier.save()
    
    if dossier.complement==None or dossier.recC==None:
        dossier.dureeC='Durée non valide'
        dossier.save()
    else:
        delta = dossier.complement - dossier.recC
        dossier.dureeC=str(delta.days)+" jours"
        dossier.save()
    
    if dossier.transmission==None or dossier.recCo==None:
        dossier.dureeCo='Durée non valide'
        dossier.save()
    else:
        delta = dossier.transmission - dossier.recCo
        dossier.dureeCo=str(delta.days)+" jours"
        dossier.save()
    
    if dossier.transmissionM==None or dossier.lancement==None:
        dossier.dureeM='Durée non valide'
        dossier.save()
    else:
        delta = dossier.transmissionM - dossier.lancement
        dossier.dureeM=str(delta.days)+" jours"
        dossier.save()

    return render(request, 'suivi/consulter_dossier.html',{'data': dossier } )

def Consulter_Budget(request,id):
    dossier = get_object_or_404(Dossier, pk=id)
    if dossier.transmissionB==None or dossier.recB==None:
        dur='Durée non valide'
    else:
        delta = dossier.transmissionB - dossier.recB
        dur=str(delta.days)+" jours"
    return render(request, 'suivi/consulter_budget.html', {'data': dossier, 'duree': dur})

def Consulter_Comptable(request,id):
    dossier = get_object_or_404(Dossier,pk=id)
    if dossier.complement==None or dossier.recC==None:
        dur='Durée non valide'
    else:
        delta = dossier.complement - dossier.recC
        dur=str(delta.days)+" jours"
    return render(request, 'suivi/consulter_comptable.html',{'data': dossier, 'duree':dur}) 

def Consulter_Commande(request,id):
    dossier=get_object_or_404(Dossier,pk=id)
    if dossier.transmission==None or dossier.recCo==None:
        dur='Durée non valide'
    else:
        delta = dossier.transmission - dossier.recCo
        dur=str(delta.days)+" jours"
    return render(request, 'suivi/consulter_commande.html', {'data': dossier, 'duree':dur})

def Consulter_Marche(request,id):
    context={}
    lots=[]
    dossier=get_object_or_404(Dossier,pk=id)
    context['dossier'] = dossier
    retirants = dossier.op_dos_set.filter(statut = 'Retirant')
    depositaires = dossier.op_dos_set.filter(statut = 'Dépositaire')
    fournisseurs = dossier.op_dos_set.filter(statut = 'Fournisseur')
    for f in fournisseurs:
        lots.append(f.lot)
    context['retirants'] = retirants
    context['depositaires'] = depositaires
    context['fournisseurs'] = fournisseurs
    context['lots'] = set(lots)
    form1 = LancementForm(instance=dossier)
    form2 = Suivi1Form(instance=dossier)
    form3 = Suivi2Form(instance=dossier)
    form4 = Suivi3Form(instance=dossier)
    form5 = Suivi4Form(instance=dossier)
    form6 = EvaluationForm(instance=dossier)
    context['form1'] = form1
    context['form2'] = form2
    context['form3'] = form3
    context['form4'] = form4
    context['form5'] = form5
    context['form6'] = form6


    return render(request, 'suivi/consulter_marche.html', context)

def Modifier_Budget(request, id):
    context={}
    obj=get_object_or_404(Dossier,pk=id)
    form = BudgetForm(request.POST or None, instance=obj)
    if form.is_valid():
        if 'transemettre' in request.POST:
            obj.service="Comptable"
            obj.save()
            messages.success(request, "Transmission avec Succées")
            return redirect('Menu_Budget')
        if 'enregistrer' in request.POST:
            obj.service="Budget"
            obj.save()
            messages.success(request, "Modification avec Succées")
        if 'cloturer' in request.POST:
            obj.statut="Annulé"
            obj.respClo=request.user.name
            obj.save()
            messages.success(request, "Cloturation avec Succées")            
        form.save()
        return redirect('Modifier_Budget',id)
    context={'form' : form ,'id' : id}
    
    return render(request, 'suivi/modif_budget.html', context)

def Modifier_Comptable(request,id):
    context={}
    obj=get_object_or_404(Dossier,pk=id)
    form = ComptableForm(request.POST or None, instance=obj)
    if form.is_valid():
        if 'transemettre' in request.POST:
            obj.service="Cloturé"
            obj.save()
            messages.success(request, "Transmission avec Succées")
        if 'enregistrer' in request.POST:
            obj.service="Comptable"
            obj.save()
            messages.success(request, "Modification avec Succées")

        form.save()
        return redirect('Modifier_Comptable',id)
    context={'form' : form, 'id' : id}
    return render(request, 'suivi/modif_comptable.html', context)


def Modifier_Marche(request,id):
    context={}
    
    obj=get_object_or_404(Dossier,pk=id)
    form = MarcheForm(request.POST or None, instance=obj)

    if form.is_valid():
        if 'transemettre' in request.POST:
            obj.service="Commande"
            obj.save()
            messages.info(request, "Modification avec Succées")
            return redirect('Menu_Marche')
        if 'enregistrer' in request.POST:
            obj.service="Marché"
            obj.save()
            messages.success(request, "Enregistrement avec Succées")
        if 'cloturer' in request.POST:
            obj.statut="Annulé"
            obj.respClo=User.__name__
            obj.save()
            messages.info(request, "Cloturation avec Succées")
            return redirect('Menu_Marche')       
        form.save()
        return redirect('Modifier_Marche', id)

    context={'form': form, 'id':id}
    return render(request, 'suivi/modif_marche.html', context)



def Modifier_Commande(request,id):
    context={}
    obj=get_object_or_404(Dossier,pk=id)
    form=CommandeForm(request.POST or None, instance=obj)
    if form.is_valid():
        if 'transemettre' in request.POST:
            obj.service="Budget"
            obj.save()
            messages.success(request, "Transmission avec Succées")
            return redirect('Menu_Commande')
        if 'enregistrer' in request.POST:
            obj.service="Commande"
            obj.save()
            messages.success(request, "Modification avec Succées")
        if 'cloturer' in request.POST:
            obj.statut="Annulé"
            obj.respClo=User.__name__
            obj.save()
            messages.success(request, "Cloturation avec Succées") 
            return redirect('Menu_Commande')
        form.save()
        return redirect('Modifier_Commande', id)

    context={'form': form, 'id':id }
    return render(request, 'suivi/modif_commande.html', context)

def Menu_Commande(request):
    context={}
    context["dataset"] = Dossier.objects.filter(service="Commande")
    

    return render(request,'suivi/menu_commande.html', context)

def Menu_precommande(request):
    context={}
    context["dataset"] = Dossier.objects.filter(Q(service = 'Commande') & Q(statut = 'Initial'))

    return render(request, 'suivi/menu_precommande.html', context)


def Precommande(request, id):
    context={}
    dossier = Dossier.objects.get(id=id)
    form = Precommande1Form(request.POST or None, instance=dossier)
    context["form"] = form
    if form.is_valid():
        form.save()
        dec = form.cleaned_data['valid_c']
        if dec == 'Oui':
            return redirect('Menu_precommande')


    return render(request, 'suivi/precommande1.html', context)

def Suivre_commande(request, id):
    context={}
    dossier = Dossier.objects.get(id=id)
    form = Suivi_commandeForm(request.POST or None, instance=dossier)
    context["form"] = form
    if form.is_valid():
        form.save()

    return render(request, 'suivi/suivre_commande.html', context)

def Menu_suivi_commande(request):
    context={}
    context["dataset"] = Dossier.objects.filter(Q(service = 'Commande') & Q(statut = 'Précommande'))

    return render(request, 'suivi/menu_suivicommande.html', context)
@login_required
def Menu_Comptable(request):
    context={}
    
    context["dataset"] = Dossier.objects.filter(service = "Comptable")

    d_list = Dossier.objects.filter(service = "Comptable").values()
    p_list=[]
    s_list=[]
    k_list=[  
            "recC",
            "respC",
            "decisionC",
            "pieces",
            "complement",
            "paiement",
            "prolongation",
            "observationsC",
        ]
    for dossier in d_list:
        c=0
        for key in dossier:
            if key in k_list:
                if  dossier[key] != None and dossier[key]!= "None" and dossier[key]!="": 
                    c+=1
        p=int(c/len(k_list)*100)
        p_list.append(p)

    i = 0
    for value in context["dataset"]:
        value.pC = p_list[i]
        if int(value.pC) <= 40:
            value.coulC="danger"
        elif int(value.pC) <= 70:
            value.coulC="warning"
        elif int(value.pC) > 70:
            value.coulC="success"
        i += 1
        
    
        
    

    return render(request,'suivi/menu_comptable.html', context)

@login_required
def Menu_Marche(request):
    context={}
    
    context["dataset"] = Dossier.objects.filter(service='Marché').order_by('-date_lanc')
    context["progress"] = {}


 

    

    return render(request,'suivi/menu_marche.html', context)

def Fournisseurs(request):
    context={}
    context["dataset"] = Operateur.objects.all()
    return render(request, 'suivi/fournisseurs.html', context)

def Ajouter_fournisseur(request):
    form = FournisseurCreationForm(request.POST or None)
    context = {}
    context['form'] = form
    if form.is_valid():
        form.save()
        messages.success(request, "Ajout du fournisseur avec Succées")
        return redirect('Fournisseurs')

    return render(request, 'suivi/add_fournisseur.html', context)

def Lancement_dossier(request):
    form = LancementForm(request.POST or None)

    context = {}
    context['form'] = form
    

    if form.is_valid():
        form.instance.service = 'Marché'
        form.instance.statut = 'Lancement'
        form.save()
        messages.success(request, "Ajout du fournisseur avec Succées")
        return redirect('Lancement_dossier_ajout_ret', form.instance.id)
        
    return render(request, 'suivi/lancement_dossier.html', context)

def Lancement_dossier_ajout_ret(request, id):
    dossier = Dossier.objects.get(id=id)
    form = Op_DosForm(request.POST or None)
    context ={}
    context['form'] = form
    context['dossier'] = dossier
    if form.is_valid():
        form.instance.dossier = dossier
        form.instance.statut = "Retirant"
        form.save()

    return render(request, 'suivi/lancement_dossier_ajout_ret.html', context)

def Supprimer_ret(request, id):
    Op_Dos.objects.get(id=id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def Ouverture_evaluation(request):
    context = {}
    
    dossiers = Dossier.objects.filter(Q(service='Marché') & (Q(statut='Lancement') | Q(statut='En ouverture') | Q(statut='En évaluation')) )
    context["dataset"] = dossiers

    return render(request, 'suivi/ouverture_evaluation.html', context)

def Acceptation(request):
    context = {}

    context['dataset'] = Dossier.objects.filter(Q(service='Marché') & (Q(statut='Accepté')))
    return render(request, 'suivi/acceptation.html', context)
    
def Infructuosite_rejet(request):
    context = {}

    context['dataset'] = Dossier.objects.filter(Q(service='Marché') & (Q(statut='Infructueux/rejeté')))
    return render(request, 'suivi/infructuosite_rejet.html', context)

def Autres(request):
    context = {}

    context['dataset'] = Dossier.objects.filter(Q(service='Marché') & (Q(statut='Autres')))
    return render(request, 'suivi/autres.html', context)

def Ouverture_evaluation_dossier(request, id):
    context={}
    obj=get_object_or_404(Dossier,pk=id)
    form = Suivi1Form(request.POST or None, request.FILES, instance=obj)
    context["dossier"] =obj
    
    context["form"] = form
    if "suivant" in request.POST:
        if form.is_valid():
            form.instance.statut = 'En ouverture'
            form.instance.service = 'Marché' 
            form.save()
            return redirect('Ouverture_dossier', id)

        
        
    return render(request, "suivi/suivre_dossier.html", context)

def Ouverture_dossier(request, id):
    context={}
    dossier = get_object_or_404(Dossier,pk=id)
    form = DepositaireForm(request.POST or None)
    context['form'] = form
    context['dossier'] = dossier
    if form.is_valid():
        form.instance.dossier = dossier
        form.instance.statut = "Dépositaire"
        form.save()
    
    return render(request, 'suivi/ouverture_dossier_ajou_depo.html', context)

def Evaluation_dossier(request, id):
    context={}
    dossier = get_object_or_404(Dossier,pk=id)
    form = EvaluationForm(request.POST or None)
    context['form'] = form
    context['dossier'] = dossier

    if form.is_valid():
        form.instance.statut = "En évaluation"
        form.save()


    return render(request, 'suivi/evaluation_dossier.html', context)

def Classement_soumissionaire(request, id):
    context={}
    dossier = get_object_or_404(Dossier,pk=id)
    context["dossier"] = dossier
    operateurs = dossier.op_dos_set.filter(statut="Dépositaire").order_by('montant')


    formset =  ClassementForm( request.POST or None) 
    if formset.is_valid():
        formset.save()
        formset.instance.statut = 'Accepté'
        dossier.save()
        messages.success(request, 'Vous avez modifé le stock avec succès')
        return redirect('Menu_Marche')

    context["ez"] = zip(operateurs,formset)
    context["formset"]=formset
    return render(request, 'suivi/classement_soumissionaire.html', context)

def Ouverture_evaluation_acceptation(request, id):
    context={}
    obj = get_object_or_404(Dossier, pk=id)
    form = Suivi2Form(request.POST or None, instance=obj)
    
    context["form"] = form
   
    if form.is_valid():

        form.save()
        messages.success(request, "Suivi avec Succées")
        if 'transmettre' in request.POST:
            form.instance.service = 'Commande'
            form.instance.statut ='Initial'
            form.save()
            return redirect('Menu_Commande')
    return render(request, "suivi/suivre_dossier_acceptation.html", context)

def Ouverture_evaluation_annulation(request, id):
    context={}
    obj = get_object_or_404(Dossier, pk=id)
    form = Suivi3Form(request.POST or None, instance=obj)
    context["form"] = form
    if form.is_valid():
        form.instance.statut = "Annulé"
        form.save()
        messages.success(request, "Suivi avec Succées")
    return render(request, "suivi/suivre_dossier_annulation.html", context)

def Ouverture_evaluation_autre(request, id):
    context={}
    obj = get_object_or_404(Dossier, pk=id)
    form = Suivi4Form(request.POST or None, instance=obj)
    context["form"] = form
    if form.is_valid():
        form.save()
        messages.success(request, "Suivi avec Succées")
    return render(request, "suivi/suivre_dossier_autre.html", context)

def Menu_Budget(request):
    context={}
    context["dataset"] = Dossier.objects.filter(service="Budget")
    d_list = Dossier.objects.filter(service="Budget").values()
    p_list=[]
    s_list=[]
    k_list=[
            "num_dossier",
            "recB",
            "respB",
            "observationB",
            "prestation",
            "définitive",
            "motifs",
            "transmissionB",
            "visa",
            "mandatement",
            "engagement",
        ]

    for dossier in d_list:
        c=0
        for key in dossier:
            if key in k_list:
                if dossier[key] != None:
                    c+=1
        p=int(c/len(k_list)*100)
        p_list.append(p)

    i = 0
    for value in context["dataset"]:
        value.pB = p_list[i]
        if int(value.pB) <= 40:
            value.coulB="danger"
        elif int(value.pB) <= 70:
            value.coulB="warning"
        elif int(value.pB) > 70:
            value.coulB="success"
        i += 1
    return render(request,'suivi/menu_budget.html', context)  

def Control_initial(request):
    context={}
    form = Control_initialForm(request.POST or None)
    context['form'] = form
    if form.is_valid():
        form.save()



    return render(request, 'suivi/control_initial.html', context) 

def Menu_Archive(request):
    data = Archive.objects.all()
    liste = []
    for q in data:
        if q.transmission == None or q.recCo == None:
            Dur = "Non valide"
        else:
            delta = q.transmission - q.recCo
            Dur = str(delta.days) + " jours"
        liste.append({
            'num_dossier': q.num_dossier,
            'recC': q.recC,
            'respC': q.respC,
            'decisionC': q.decisionC,
            'pieces': q.pieces,
            'complement': q.complement,
            'paiement': q.paiement,
            'prolongation': q.prolongation,
            'observationsC': q.observationsC,
            'dureeC': q.dureeC,
            'type_dossier': q.type_dossier,
            'objet': q.objet,
            'lancement': q.lancement,
            'ouverture': q.ouverture,
            'observationM': q.observationM,
            'fournisseur': q.fournisseur,
            'transmissionM': q.transmissionM,
            'decisionM': q.decisionM,
            'convention': q.convention,
            'respM': q.respM,
            'dureeM': q.dureeM,
            'recCo': q.recCo,
            'respCo': q.respCo,
            'decisionCo': q.decisionCo,
            'observation': q.observation,
            'proformaCo': q.proformaCo,
            'dproforma': q.dproforma,
            'montant': q.montant,
            'bonc': q.bonc,
            'dbonc': q.dbonc,
            'prestation': q.prestation,
            'définitive': q.définitive,
            'bonr': q.bonr,
            'transmission': q.transmission,
            'dureeCo': q.dureeCo,
            'recB': q.recB,
            'respB': q.respB,
            'observationB': q.observationB,
            'engagement': q.engagement,
            'motifs': q.motifs,
            'visa': q.visa,
            'transmissionB': q.transmissionB,
            'dureeB': q.dureeB,
            'mandatement': q.mandatement,
            'service': q.service,
            'motifClo': q.motifClo,
            'respClo': q.respClo,
            'statut': q.statut,
            'duree': q.duree,
            'Dur': Dur,

        })
    return render(request, 'suivi/menu_archive.html', {'data': liste})

def Requete(request):
    list = Dossier.objects.all()
    filter = RequeteFilter(request.GET, queryset=list)


    return render(request,'suivi/statistiques.html',{'filter': filter}) 


def Control(request):
    context={}
    context["dataset"] = Dossier.objects.all()

    return render(request,'suivi/control.html', context)






