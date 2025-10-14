from django.contrib import admin

from planification.models import Indicateur
from programme.models import ComposantesProgram, Action, Activite, IndicateurProgram, DomainResult, SousDomainResult, \
    TacheProgram, PlanificationCoutProgram


@admin.register(ComposantesProgram)
class ComposantesProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'label','description')


@admin.register(DomainResult)
class DomainResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'label','description')


@admin.register(SousDomainResult)
class SousDomainResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'label','description')

@admin.register(IndicateurProgram)
class IndicateurProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'label','cible','base')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'description','indicateur')


@admin.register(TacheProgram)
class TacheProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'label','description','activite','indicateur')


@admin.register(PlanificationCoutProgram)
class PlanificationCoutProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'frequence','unite','cout_unitaire','duree')