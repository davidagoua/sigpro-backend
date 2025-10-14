from django.core.management.base import BaseCommand
from core.services import upload_ptba
from test import ingest
from planification.models import Exercice




class Command(BaseCommand):
    help = 'Crée les départements spécifiés'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Création des exercices"))
        Exercice.objects.create(label="2024", date_debut="2024-01-01", date_fin="2024-12-31")
        Exercice.objects.create(label="2025", date_debut="2025-01-01", date_fin="2025-12-31")
        self.stdout.write(self.style.SUCCESS("Ingestion PTBA projet"))
        result = upload_ptba()
        self.stdout.write(self.style.SUCCESS(result))
        self.stdout.write(self.style.SUCCESS('Ingestion PTBA programme'))
        ingest('programme')
        self.stdout.write(self.style.SUCCESS("Ingestion Terminée"))