from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


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








