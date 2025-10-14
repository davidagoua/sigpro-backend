from django.core.management.base import BaseCommand
from core.models import Role  # Remplacez 'your_app' par le nom de votre application

class Command(BaseCommand):
    help = 'Crée les départements spécifiés'

    def handle(self, *args, **kwargs):
        # Liste des départements à créer
        roles = [
            "PointFocal",
            "DirecteurLocal",
            "Directeur",
            "DirecteurExe"
        ]
        
        count = 0
        # Parcours de la liste et création des départements
        for dept_name in roles:
            # Vérifie si le département existe déjà
            if not Role.objects.filter(name=dept_name).exists():
                # Crée le département s'il n'existe pas
                Role.objects.create(name=dept_name)
                self.stdout.write(self.style.SUCCESS(f'Role "{dept_name}" créé avec succès'))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Le Role "{dept_name}" existe déjà'))
        
        self.stdout.write(self.style.SUCCESS(f'{count} Role ont été créés'))