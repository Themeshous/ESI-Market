
from tabnanny import verbose
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import AbstractUser, User
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import OneToOneField
from django.utils import timezone

from django.contrib.auth.models import Group
from django.utils.duration import duration_string



class Lot(models.Model):
    designation = models.CharField("Désignation du lot",max_length=30, blank=True, null=True)
    def __str__(self):
        return str(self.designation)

class Operateur(models.Model):
    def __str__(self):
        return str(self.op)
    op = models.CharField("Opérateur", blank=True, null=True, max_length=30)
    nif = models.CharField("Numéro d'identification fiscale", blank=True, null=True, max_length=30)
    adresse = models.CharField("Adresse", blank=True, null=True, max_length=30)
    tel = models.CharField("Téléphone", blank=True, null=True, max_length=30)
    email = models.CharField("Email", blank=True, null=True, max_length=30)
    CHOIX5 = (
        ('sarl','sarl'),
        ('eurl', 'eurl'),
        ('spa', 'spa'),
    )
    form_ju = models.CharField("Forme juridique",choices=CHOIX5, blank=True, null=True, max_length=30)
    nom_prop_ger = models.CharField("Nom du propriétaire ou du gérant", blank=True, null=True, max_length=30)
    reg_comm = models.CharField("Registre de commerce", blank=True, null=True, max_length=30)
    deg_qual = models.CharField("Degré de la qualification professionnelle (pour les ETB-TCE)", blank=True, null=True, max_length=30)
   
    moy_chif = models.CharField("Bilans des trois dernières années (moyenne du chiffre d'affaires) ", blank=True, null=True, max_length=30)
    note_eval = models.IntegerField("Note d'évaluation", blank=True, null=True)





class Dossier(models.Model):
    #Service Marché
    #Lancement---------------
    num_dossier=models.CharField("Numéro du dossier", max_length=30,blank=True,null=True)
    objet = models.CharField("Objet", max_length=60, null=True, blank=True)
    agent_fichtech = models.CharField("Nom de l'agent ayant validé la fiche technique", max_length=20,blank=True,null=True)
    date_valid_fichtech = models.DateField("Date de validation de la fiche technique", blank=True,null=True)
    fich_tech = models.FileField(verbose_name="Fiche technique validée", upload_to='storage', null=True, blank=True)
    date_lanc=models.DateField('Date de lancement',blank=True,null=True)
    operateurs = models.ManyToManyField(Operateur, verbose_name="Liste des soumissionaires ayant retiré la fiche technique", blank=True)
    #------------------------
    #Ouverture et Evalutation---------------------------------------
    ancien_num = models.CharField("Ancien numéro du dossier", max_length=30,blank=True,null=True)

    resp_suivi_m = models.CharField("Responsable du suivi du dossier", max_length=20,blank=True,null=True)
    resp_qual = models.CharField("Responsable de qualité", max_length=20,blank=True,null=True)
    
    ouverture=models.DateField('Date d\'ouverture',blank=True,null=True)
    CHOIX = (
        ('',''),
        ('Acceptation','Acceptation'),
        ('Infructuosité','Infructuosité'),
        ('Annulation/rejet', 'Annulation/rejet'),
        ('Autre', 'Autre')
    )
    dec=models.CharField("Décision",max_length=20,choices=CHOIX,blank=True,null=True)
    obs_ouver = models.TextField("Observation d'ouverture", blank=True, null=True)
    date_depo_offre = models.DateTimeField("Date et heure de déposition des offres", blank=True, null=True)
    date_ouverture_plis = models.DateTimeField("Date et heure de l'ouverture des plis", blank=True, null=True)
    
    #-------------------------------------------
    #Acceptation-------
   
    date_eval = models.DateField("Date d'évaluation", blank=True, null=True)
    obs_eval = models.TextField("Observation d'évaluation", blank=True, null=True)
    bord_dos_m = models.FileField("Bordereau dossier (marché)", upload_to='storage', blank=True, null=True)
    
    desist_soum = models.TextField("En cas de désistement de soumissionnaire", blank=True, null=True)
    letr_desist = models.FileField("Lettre de désistement", upload_to='storage', null=True, blank=True)
    num_contrat = models.CharField("N° de Contrat",max_length=30, blank=True, null=True)
    CHOIX2 = (
        ('',''),
        ('Système de notation','Système de notation'),
        ('Le moins Disant', 'Le moins Disant'),
    )
    sys_eval = models.CharField("Système d'évaluation", max_length=30, choices=CHOIX2, blank=True, null=True)
    pv_eval = models.FileField("PV Evaluation", upload_to='storage', blank=True, null=True)
    autre_docs = models.FileField("Autres Documents", upload_to='storage', max_length=10, null=True, blank=True)
    rapp_present = models.FileField("Rapport de présentation", upload_to='storage', blank=True, null=True)
    contrat = models.FileField("Contrat", upload_to='storage', null=True, blank=True)
    dos_trans = models.FileField("Dossier complet envoyé vers le service commande", upload_to='storage', blank=True, null=True)
    date_trans_comm = models.DateField('Date de transmission au service commande',blank=True,null=True)
    #--------------------------------
    #Annulation et Infructuosité/Rejet----------------------
    obs_annul = models.TextField("Observations (Infructuosité/Annulation)", blank=True,null=True )
    pv_infruc = models.FileField("PV d'infructuosité",upload_to='storage', null=True, blank=True)
    pv_annul = models.FileField("PV d'annulation", upload_to='storage', blank=True, null=True)
    #--------------------------------
    #Autres------------------------
    obsM = models.TextField('Observations',blank=True,null=True)
    #-------------------------------

    #Service commande
    #Pré-commande
    CHOIX3 = (
        ('Commande consultation','Commande consultation'),
        ('Commande directe','Commande directe'),
        ('',''),
    )
    typ_comm = models.CharField("Types de commande", choices= CHOIX3, max_length=30, blank=True, null=True)
    date_rec_comm = models.DateField("Date de réception du dossier au service commandes", blank=True, null=True)
    resp_suivi_C=models.CharField("Responsable du suivi au service commandes",max_length=30,blank=True,null=True)
    resp_qual_C = models.CharField("Responsable de qualité au service commandes", max_length=30, blank=True, null=True)
    bord_dos_c = models.CharField("Borderau du dossier (commandes)", max_length=30, blank=True, null=True)
    obs_c = models.TextField("Observations", blank=True, null=True)
    CHOIX4 = (
        ('Oui', 'Oui'),
        ('Non', 'Non')
    )
    valid_c = models.CharField("Dossier valide pour l’envoi au service budget ?",choices=CHOIX4, max_length=30, blank=True, null=True)
    # Oui
    num_fac_prof = models.CharField("N° de facture proforma", max_length=30, blank=True, null=True)
    date_fac_prof = models.DateField("Date de la facture proforma", blank=True, null=True)
    montant_c = models.CharField("Montant", max_length=30, blank=True, null=True)
    num_bon_comm = models.CharField("N° Bon de Commande", max_length=30, null=True, blank=True)
    date_trans_budget = models.DateField("Date d'envoi au service Budget", blank=True, null=True)
    # Non
    date_retour_marche = models.DateField("Date de retour au service marché", blank=True, null=True)
    motif_retour_marche = models.TextField("La raison de retour du dossier", blank=True, null=True)
    # Suivi commandes
    date_bon_comm = models.DateField("Date de signature du bon de commande", blank=True, null=True)
    bon_comm = models.FileField("Bon de commande signé", upload_to='storage', blank=True, null=True)
    obs_suivi_comm = models.TextField("Observations sur le suivi des commandes", blank=True, null=True)
    num_fac_def = models.CharField("N° de facture définitive", max_length=30, blank=True, null=True)
    date_fac_def = models.DateField("Date Facture définitive", blank=True, null=True)
    montant_fac_def = models.CharField("Montant",max_length=30, blank=True, null=True)
    date_rec_prest = models.DateField("Date de réception de prestation", blank=True, null=True)
    num_bon_rec = models.CharField("N° bon de réception", max_length=30, blank=True, null=True)
    obs_prest = models.TextField("Observations sur la prestation", blank=True, null=True)
    doc_just_prest = models.FileField("Document justifiant le déroulement de la prestation", upload_to='storage', blank=True, null=True)
    bord_envoi = models.FileField("Bordereau d'envoi", upload_to='storage', blank=True, null=True)
    date_trans_budget2 = models.DateField("Date d'envoi au service Budget", blank=True, null=True)
    # Control initial 
    date_rec_budg = models.DateField("Date de réception du dossier au service budget", null=True, blank=True)
    resp_suivi_b = models.CharField("Responsable du suivi du dossier dans le service budget",max_length=30, blank=True, null=True)
    resp_qual_b = models.CharField("Responsable qualité dans le service budget",max_length=30, blank=True, null=True)
    dec_b = models.CharField("Décision", max_length = 30, blank=True, null=True)
    date_clot_init = models.CharField("Date de clôture du contrôle initial", max_length=30, blank=True, null=True)
    obs_rejet_budg = models.TextField("Observations sur la décision en cas de rejet", blank=True, null=True)
    date_retour_comm = models.DateField("Date de retour au service commandes", blank=True, null=True)
    #  Finalisation dossier
    type_paiement = models.CharField("Type de paiement",max_length=30, blank=True, null=True)
    date_eng_cf = models.DateField("Date d'engagement au CF", blank=True, null=True)
    motif_rejet = models.TextField("Motifs de rejet éventuel", blank=True, null=True)
    date_visa = models.DateField("Date de visa", blank=True, null=True)
    date_mandat = models.DateField("Date de Mandatement", blank=True, null=True)
    date_sign_mand = models.DateField("Date de signature du mandat", blank=True, null=True)
    mandat = models.FileField("Mandat de paiement signé", upload_to='storage', blank=True, null=True)
    bord_dos_b = models.FileField("Bordereau d'envoi", upload_to='storage', blank=True, null=True)
    date_trans_compt = models.DateField("Date de transmission à l'agent comptable", blank=True, null=True)
    obs_b_rejet = models.TextField("Observations sur la décision en cas de rejet", blank=True, null=True)
    fich_regul = models.FileField("Fiche de régularisation signé", upload_to='storage', blank=True, null=True)
    #-----------------------------------------------------------------
    # Service comptable
    date_rec_compt = models.DateField("Date de réception au service comptable", blank=True, null=True)
    resp_compt = models.CharField("Responsable du suivi du dossier au service comptable",max_length=30, blank=True, null=True)
    resp_qual_compt = models.CharField("Responsable Qualité au service comptable", max_length=30, blank=True, null=True)
    dec_compt = models.CharField("Décision (service comptable)",max_length=30, blank=True, null=True)
    bord_dos_compt = models.FileField("Bordereau du dossier au service comptable", upload_to='storage', blank=True, null=True)
    motif_rejet_compt = models.TextField("Motif du rejet éventuel", blank=True, null=True)
    note_rejet = models.FileField("Note de rejet éventuel scannée", upload_to='storage', blank=True, null=True)
    obs_piec_complet = models.TextField("Observations (Pièces à compléter)", blank=True, null=True)
    date_retour_budg = models.DateField("Date de retour au service budget", blank=True, null=True)
    date_paiement = models.DateField("Date du paiement", blank=True, null=True)

    def __str__(self):
        return 'Dossier: '+str(self.num_dossier)

    service=models.TextField(max_length=30,blank=True, null=True)
    statut=models.TextField(max_length=30,blank=True, null=True)
    lots = models.ManyToManyField(Lot, verbose_name="Lots", blank=True)

class Op_Dos(models.Model):
    def __str__(self):
        return str(self.op)
    op = models.ForeignKey(Operateur, verbose_name="Opérateur", blank=True, null=True, on_delete=models.CASCADE)
    dossier = models.ForeignKey(Dossier, verbose_name="Dossier", blank=True, null=True, on_delete=models.CASCADE)
    CHOIX6 = (
        ('Retirant', 'Retirant'),
        ('Dépositaire', 'Dépositaire'),
        ('Fournisseur', 'Fournisseur')
    )
    statut = models.CharField("Statut de l'opérateur au niveau du dossier", choices=CHOIX6, blank=True, null=True, max_length = 30)
    lot = models.ForeignKey(Lot, verbose_name="Lot choisi par le dépositaire", blank=True, null=True, on_delete=models.CASCADE)
    montant = models.CharField("Montant de l'offre déposée", blank=True, null=True, max_length=30)
    ordre = models.IntegerField("Ordre du soumissionaire", blank=True, null=True)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    adresse = models.CharField('Adresse',max_length=30,blank=True, null=True)
    num = models.CharField('Numéro de Téléphone',max_length=30,blank=True, null=True)
    CHOIX2 = (
        ('Administrateur','Administrateur'),
        ('Consultation','Consultation'),
        ('Consultation/Modification','Consultation/Modification'),
        ('Ordonnateur','Ordonnateur'),
    )  
    profil = models.CharField('Type du Profile',choices=CHOIX2,max_length=30,blank=True,null=True)

    
    def __str__(self):
        return 'User: '+str(self.user)

class Utils(models.Model):
    year =models.DateField('L\'année commerciale actuelle')
    dm = models.IntegerField('Durée de traitement de Dossiers du service marché')
    db = models.IntegerField('Durée de traitement de Dossiers du service budget')
    dc = models.IntegerField('Durée de traitement de Dossiers du service comptable')
    dco = models.IntegerField('Durée de traitement de Dossiers du service commande')

class Checkbox_m(models.Model):
    
    models.BooleanField('Objet de la consultation', blank=True, null =True)
    models.BooleanField('Date de consultation', blank=True, null =True)
    models.BooleanField('Date de dépot', blank=True, null =True)
    models.BooleanField('Dossier de soumission', blank=True, null =True)
    models.BooleanField('La fiche technique', blank=True, null =True)
    models.BooleanField('La date et l\'heure d\'ouverture et d\'évaluation', blank=True, null =True)
    models.BooleanField('Le numéro et l\'objet de consultation', blank=True, null =True)
    models.BooleanField('La date en lettres', blank=True, null =True)
    models.BooleanField('Vérification de l\'orde du jour', blank=True, null =True)
    models.BooleanField('Les membres présents et leur signature', blank=True, null =True)
    models.BooleanField('Nombre de consultation retirées', blank=True, null =True)
    models.BooleanField('Nombre de plis dépoisés', blank=True, null =True)
    models.BooleanField('Listes des soumissionnaires par ordres d\'arrivées', blank=True, null =True)
    models.BooleanField('Les montants', blank=True, null =True)

