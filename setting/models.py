
from django.db import models



class VehiculeDisponible(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='disponible')


class Vehicule(models.Model):
    model = models.CharField(max_length=100)
    annee = models.IntegerField()
    marque = models.CharField(max_length=100)
    immatriculation = models.CharField(max_length=100)
    numero_chassis = models.CharField(max_length=100)
    entretients = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=100, null=False, blank=True, default='disponible')


    def __str__(self) -> str:
        return f'{self.marque} {self.model} {self.annee}'



class EmpruntVehicule(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    date_sortie = models.DateTimeField()
    date_retour = models.DateTimeField(null=True, blank=True)
    type_sortie = models.CharField(max_length=100, choices=[
        ('mission', 'Mission'),
        ('course', 'Course'),
        ('deplacement', 'Deplacement'),
    ])
    destination = models.JSONField(max_length=100, null=True, blank=True)

    nom_prenom = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nom & prenoms Responsable')
    nom_chauffeur = models.CharField(max_length=100)
    mission = models.TextField(null=True, blank=True)
    km_in = models.PositiveIntegerField(default=0, null=True, blank=True)
    km_out = models.PositiveIntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=100, default='En poul', blank=True, null=True)
    is_panne = models.BooleanField(default=False)
    type_panne = models.CharField(max_length=100, null=True, blank=True, verbose_name="Incidents", choices=[
        ('panne_seche', "Panne séche"),
        ('crevaison', "Crevaison"),
        ('Pièces retirée', "Pièce Retirer"),
        ('autres', "Autres"),
    ])


    def __str__(self) -> str:
        return f"{self.vehicule} - {self.nom_prenom} - {self.nom_chauffeur} - {self.mission} - {self.date_sortie} - {self.date_retour}"
