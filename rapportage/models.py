from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from core.models import Departement, Role
import urllib.parse



User = get_user_model()



class TypeRapport(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class Rapport(TimeStampedModel, models.Model):

    type_choices = models.TextChoices('type', names=[
        'Mensuel-Projet',
        'Trimestriel-Projet',
        'Mensuel-Programme',
        'Trimestriel-Programme',
        'Semestriel',
        'Annuel',
        'Circonstancier',
      
    ])

    file = models.FileField(verbose_name='Fichier', upload_to='rapports')
    label = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.IntegerField(default=0)
    type = models.CharField(max_length=100, null=True, blank=True, choices=type_choices)
    departements = models.ManyToManyField(Departement)
    roles = models.ManyToManyField(Role)
    status = models.IntegerField(default=0)

    @property
    def generate_collabora_url(self):
        base_url = "https://collabora.sigpro-mena.com/browser/ded56d8ff7/cool.html?WOPISrc="  # Remplacez par l'URL de votre serveur Collabora Online
        wopi_src = urllib.parse.quote_plus(f"https://sigpro-mena.com/rapportage/wopi/files/{self.id}")  # Remplacez par l'URL de votre vue WOPI
        url = f"{base_url}{wopi_src}"
        return url

    def __str__(self):
        return f'{self.type} - {self.state}'


