from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django_extensions.db.models import TimeStampedModel

#from core.services import upload_ptba


class Role(models.Model):
    name = models.CharField(max_length=120)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name


class Departement(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    contact = models.CharField(max_length=120)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, null=True, blank=True)


class Exercice(TimeStampedModel, models.Model):
    label = models.CharField(max_length=100, verbose_name="Année")
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_total = models.BigIntegerField(default=0)
    status = models.IntegerField(default=0)
    file = models.FileField(null=True, blank=True, verbose_name="Fichier Excel")

    def __str__(self):
        return str(self.label)

    @property
    def montant_planifier(self) -> int:
        return sum(tache.montant_planifier for tache in self.planificationcout_set.filter(status__gte=30))

    @property
    def montant_engage(self) -> int:
        return sum(tache.montant_engage for tache in self.tache_set.filter(status=30))

    @property
    def somme_drf(self) -> int:
        return sum(
            tache.total_decaissement for tache in self.tache_set.filter(status=30)
        )

    @property
    def reste_a_payer(self) -> int:
        return self.montant_engage - self.somme_drf

    @property
    def reste_a_planifier(self) -> int:
        return self.montant_total - self.montant_engage

    def save(self, *args, **kwargs):
        #upload_ptba(self.file)
        return super().save(*args, **kwargs)
