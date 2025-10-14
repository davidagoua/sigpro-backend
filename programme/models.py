from django.db import models
from django_extensions.db.models import TimeStampedModel


from planification.models import Exercice


class ComposantesProgram(models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    sous_domain = models.ForeignKey('SousDomainResult', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self): return self.label

class DomainResult(models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.label


class SousDomainResult(models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField()
    domain = models.ForeignKey(DomainResult, on_delete=models.CASCADE)
    result = models.TextField()

    def __str__(self):
        return self.label


class IndicateurProgram(TimeStampedModel,models.Model):
    label = models.CharField(max_length=100)
    base = models.FloatField(default=0)
    cible = models.FloatField(default=0)
    order = models.CharField(max_length=100)
    sous_domain = models.ForeignKey(SousDomainResult, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

class Action(TimeStampedModel,models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    composante = models.ForeignKey(ComposantesProgram, on_delete=models.CASCADE)

    def __str__(self): return self.label


class Activite(TimeStampedModel,models.Model):
    label = models.CharField(max_length=100)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    description = models.TextField()
    localisation = models.TextField(max_length=100)
    type_activite = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    indicateur = models.ForeignKey(IndicateurProgram, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(default=0)
    status_execution = models.IntegerField(default=0)
    ref_ddp = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_nature = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_action = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_activites = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_ligne = models.CharField(max_length=100, null=True, blank=True)
    ppm = models.CharField(max_length=100, null=True, blank=True)
    responsable = models.ForeignKey('core.Departement', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.label

    @property
    def is_sous(self):
        return (self.label).lower().__contains__('sous')


class Quarter(TimeStampedModel,models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.SET_NULL, null=True, blank=True)
    label = models.CharField(max_length=100)
    annee = models.IntegerField()

    def __str__(self):
        return f'{self.exercice} - {self.label}'


class ActiviteMonth(TimeStampedModel,models.Model):
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(default=0)


class TacheProgram(TimeStampedModel,models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField()
    responsable = models.CharField(max_length=100, null=True, blank=True)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    location = models.TextField(max_length=100, null=True, blank=True)
    partenaire = models.CharField(max_length=100, null=True, blank=True)
    indicateur = models.ForeignKey(IndicateurProgram, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_nature = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_action = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_activites = models.CharField(max_length=100, null=True, blank=True)
    ref_ddp_ligne = models.CharField(max_length=100, null=True, blank=True)
    ppm = models.CharField(max_length=100, null=True, blank=True)
    order = models.CharField(max_length=100, null=True, blank=True)
    nature_economique = models.CharField(max_length=100, null=True, blank=True)




class PlanificationCoutProgram(TimeStampedModel,models.Model):
    montant = models.FloatField(default=0, null=True, blank=True)
    unite = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.FloatField(default=1, null=True, blank=True)
    frequence = models.CharField(default=0, max_length=100, null=True, blank=True)
    duree = models.FloatField(default=0, null=True, blank=True)
    tache = models.ForeignKey(TacheProgram, on_delete=models.CASCADE)
    cout_unitaire = models.FloatField(default=0, null=True, blank=True)
    exercice = models.ForeignKey(Exercice, on_delete=models.SET_NULL, null=True, blank=True)

    def cout_total(self):
        return self.cout_unitaire * self.quantity * self.frequence * self.duree

    def __str__(self):
        return f'{self.tache} - {self.unite} - {self.quantity} - {self.frequence} - {self.duree}'