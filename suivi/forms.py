

from cProfile import label
from dataclasses import field
from pyexpat import model
from django import forms
from django.forms import fields
from django.forms.models import ALL_FIELDS
from matplotlib import widgets
from .models import Dossier, Op_Dos, Operateur, Utils
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User,Group
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.forms import modelformset_factory



class UserForm(UserCreationForm):
    group = forms.ModelMultipleChoiceField(label='Services',queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','password1','password2','group']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name', 'last_name','username','password1','password2','group']:
            self.fields[fieldname].help_text = None

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','groups']
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name', 'last_name','password', 'username','groups']:
            self.fields[fieldname].help_text = None

    
class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['adresse', 'num','profil']
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['adresse', 'num','profil']


class UtilsForm(forms.ModelForm):
    class Meta:
        model=Utils
        fields=['dm','db','dc','dco']

# Service Marché
class FournisseurCreationForm(forms.ModelForm):
    class Meta:
        model= Operateur
        fields = '__all__'
        exclude = ('dossier',)

class LancementForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['num_dossier','ancien_num','objet', 'agent_fichtech', 'date_valid_fichtech', 'fich_tech', 'date_lanc','service','statut']
        widgets = {
            'date_lanc' : forms.DateInput(attrs={'type': 'date'}),
            'service': forms.HiddenInput,
            'statut': forms.HiddenInput,
            'date_valid_fichtech' : forms.DateInput(attrs={'type': 'date'}),
            
        }

class Op_DosForm(forms.ModelForm):
    class Meta:
        model = Op_Dos
        fields = '__all__'
        exclude = ['dossier','lot','montant','statut','ordre']


class DepositaireForm(forms.ModelForm):
    class Meta:
        model = Op_Dos
        fields = '__all__'
        exclude = ['dossier', 'statut','ordre']


class Suivi1Form(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['date_depo_offre', 'date_ouverture_plis','obs_ouver', 'resp_suivi_m', 'resp_qual', 'ouverture', 'service' ]
        widgets = {
            'service':forms.HiddenInput,
            'statut': forms.HiddenInput,
            
            'date_depo_offre' : forms.DateInput(attrs={'type': 'datetime-local'}),
            'date_ouverture_plis' : forms.DateInput(attrs={'type': 'datetime-local'}),
            'ouverture' : forms.DateInput(attrs={'type': 'date'}),
            
            
        }



class Suivi2Form(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['obs_ouver', 'date_eval', 'bord_dos_m', 'letr_desist', 'num_contrat', 'sys_eval', 'pv_eval', 'autre_docs', 'rapp_present', 'contrat','date_trans_comm']
        widgets = {
            'date_eval': forms.DateInput(attrs={'type': 'date'}),
            
        }

class Suivi3Form(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['obs_annul', 'pv_infruc', 'pv_annul']

class Suivi4Form(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['obsM']

# Service commandes
class Precommande1Form(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['typ_comm', 'num_dossier', 'date_rec_comm','resp_suivi_C', 'resp_qual_C','bord_dos_c', 'obs_c', 'valid_c']
        widgets = {
            'date_rec_comm' : forms.DateInput(attrs={'type': 'date'})
        }

class Precommande2Form(forms.ModelForm):
    class Meta:
        model = Dossier
        fields=['num_fac_prof','date_fac_prof' , 'montant_c', 'num_bon_comm', 'date_trans_budget']
        widgets = {
            'date_fac_prof' : forms.DateInput(attrs={'type': 'date'}),
            'date_trans_budget': forms.DateInput(attrs={'type': 'date'}),
        }
class Precommande3Form(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['date_retour_marche', 'motif_retour_marche']
        widgets = {
            'date_retour_marche' : forms.DateInput(attrs={'type': 'date'})
        }

class Suivi_commandeForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['num_dossier','date_bon_comm', 'bon_comm', 'obs_suivi_comm', 'num_fac_def', 'date_fac_def', 'montant_fac_def', 'date_rec_prest', 'num_bon_rec', 'obs_prest', 'doc_just_prest', 'bord_envoi', 'date_trans_budget2']
        widgets = {
            'date_bon_comm' : forms.DateInput(attrs={'type': 'date'}),
            'date_fac_def' : forms.DateInput(attrs={'type': 'date'}),
            'date_rec_prest' : forms.DateInput(attrs={'type': 'date'}),
            'date_trans_budget2' : forms.DateInput(attrs={'type': 'date'}),
        }
# Service budget

class Control_initialForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['num_dossier','date_rec_budg', 'resp_suivi_b', 'resp_qual_b', 'dec_b', 'date_clot_init', 'obs_rejet_budg', 'date_retour_comm']
        widgets={
            'date_rec_budg' : forms.DateInput(attrs={'type': 'date'}),
            'date_retour_comm' : forms.DateInput(attrs={'type': 'date'}),
        }

class FinalisationForm(forms.ModelForm):
    class Meta:
        models = Dossier
        fields = ['num_dossier', 'type_paiement', 'date_eng_cf', 'motif_rejet']

class Comptable1Form(forms.ModelForm):
    class Meta:
        models = Dossier
        fields = ['num_dossier', 'date_rec_compt', 'resp_compt', 'resp_qual_compt','dec_compt']

class Comptable2Form(forms.ModelForm):
    class Meta:
        models = Dossier
        field = ['bord_dos_compt', 'motif_rejet_compt', 'note_rejet', 'obs_piec_complet', 'date_retour_budg']

class Comptable3Form(forms.ModelForm):
    class Meta:
        models = Dossier
        field = ['date_paiement']
    
class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['date_eval', 'obs_eval']
        widgets = {
            'date_eval': forms.DateInput(attrs={'type': 'date'}),
        }

ClassementForm = modelformset_factory(Op_Dos, fields={"ordre"})