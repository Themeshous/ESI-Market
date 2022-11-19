from random import choices
import django_filters
from django import forms
from suivi.models import Dossier
class RequeteFilter(django_filters.FilterSet):
    CHOIX1 = (
        ('Marché','Marché'),
        ('Consultation','Consultation'),
        ('Gré à gré','Gré à gré'),
    )
    CHOIX2 =(
        ('Marché','Marché'),
        ('Budget','Budget'),
        ('Commande','Commande'),
        ('Comptable','Comptable'),
    )   
    CHOIX3 =(
        ('En cours','En cours'),
        ('En retard','En retard'),
        ('Cloturé','Cloturé'),
        ('Annulé','Annulé'),
    ) 
    lancement=django_filters.DateFromToRangeFilter(label='Période')
    type_dossier=django_filters.ChoiceFilter(choices=CHOIX1)
    respM=django_filters.AllValuesFilter(label='Responsable du dossier sous le service marché')
    respCo=django_filters.AllValuesFilter(label='Responsable du dossier sous le service comptabilité')
    respB=django_filters.AllValuesFilter(label='Responsable du dossier sous le service budget')
    respC=django_filters.AllValuesFilter(label='Responsable du dossier sous le service commande')
    service = django_filters.ChoiceFilter(choices=CHOIX2, label='Service Actuel')
    statut = django_filters.ChoiceFilter(choices=CHOIX3)
    class Meta:
        model=Dossier
        fields=['service','respM','respCo','respB','respC','statut','type_dossier']