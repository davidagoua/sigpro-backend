from django.core.management.base import BaseCommand
from core.models import Departement  # Remplacez 'your_app' par le nom de votre application

class Command(BaseCommand):
    help = 'Crée les départements spécifiés'

    def handle(self, *args, **kwargs):
        # Liste des départements à créer
        departments = [
            "DSPA",
            "DAAJE",
            "DENF",
            "DMDA",
            "DMOSS",
            "DAPS-COGES",
            "DESPS",
            "DPFC",
            "DVSP",
            "CAC-RE",
            "SE COP",
            "DEEG",
            "DAF",
            "DELC",
            "DAJC",
            "DECO",
            "DRH",
            "DTSI",
            "IGENA",
            "DCEP",
            "SCRP",
            "DEEP",
            "SIDI",
            "SGP",
            "CPPM"
        ]
        
        count = 0
        # Parcours de la liste et création des départements
        for dept_name in departments:
            # Vérifie si le département existe déjà
            if not Departement.objects.filter(name=dept_name).exists():
                # Crée le département s'il n'existe pas
                Departement.objects.create(name=dept_name)
                self.stdout.write(self.style.SUCCESS(f'Département "{dept_name}" créé avec succès'))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Le département "{dept_name}" existe déjà'))
        
        self.stdout.write(self.style.SUCCESS(f'{count} départements ont été créés'))