from django.core.management.base import BaseCommand
from core.models import Role, Departement
from planification.models import SousComposantProjet, ComposantProjet, Tache, Decaissement, Exercice, Indicateur
from programme.models import *
from suivi.models import *
from planification.models import *

class Command(BaseCommand):
    help = 'Crée les départements spécifiés'

    def handle(self, *args, **kwargs):
        # supprimer les données
        self.stdout.write(self.style.SUCCESS('Suppression des données'))
        Tache.objects.all().delete()
        
        Departement.objects.all().delete()
        Indicateur.objects.all().delete()
        Activite.objects.all().delete()
        Exercice.objects.all().delete()
        TDRProgramme.objects.all().delete()
        SousComposantProjet.objects.all().delete()
        ComposantProjet.objects.all().delete()
        Tache.objects.all().delete()
        Decaissement.objects.all().delete()
        TDR.objects.all().delete()
        CommentaireTDR.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Donnees supprimées'))
        
        