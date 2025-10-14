from django.contrib import admin
from .models import PTBAProjet, ComposantProjet, SousComposantProjet, Tache, \
    Indicateur, Exercice, PlanificationCout
from .models import CategorieDepense, TypeUnite, TypeProcedureAcquisition, Decaissement, TypeUGP

@admin.register(PTBAProjet)
class PTBAProjetAdmin(admin.ModelAdmin):
    list_display = ('montant_total', 'created', 'modified')
    list_filter = ('created',)
    date_hierarchy = 'created'


@admin.register(ComposantProjet)
class ComposantProjetAdmin(admin.ModelAdmin):
    list_display = ('label', 'ptba', 'created')
    search_fields = ('label',)
    list_filter = ('ptba',)






@admin.register(SousComposantProjet)
class SousComposantProjetAdmin(admin.ModelAdmin):
    list_display = ('label', 'sigle', 'composant', 'created')
    search_fields = ('label', 'sigle')
    list_filter = ('composant',)





@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('label', 'date_debut', 'date_fin',)
    search_fields = ('label',)
    list_filter = ('created',)
    date_hierarchy = 'created'


class PlanificationCoutAdmin(admin.TabularInline):
    model = PlanificationCout
    extra = 0

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('label', 'type', 'categorie', 'indicateur', 'status', 'unite', 'montant_engage', 'cout', 'quantite', 'ugp', 'date_debut', 'date_fin', 'responsable')
    list_filter = ('type', 'categorie', 'indicateur', 'status', 'unite', 'ugp')
    search_fields = ('label', 'responsable')
    date_hierarchy = 'date_debut'
    filter_horizontal = ('depends_on',) # Use for ManyToMany fields
    fieldsets = (
        (None, {'fields': ('exercice',)}),
        ('Informations générales', {
            'fields': ('label', 'type', 'categorie', 'indicateur', 'unite', 'ugp', 'responsable')
        }),
        ('Détails financiers', {
            'fields': ('montant_engage', 'cout', 'quantite')
        }),
        ('Planification', {
            'fields': ('date_debut', 'date_fin', 'frequence')
        }),
        ('Statut et dépendances', {
            'fields': ('status', 'depends_on','departement')
        }),
    )
    inlines = [PlanificationCoutAdmin]


@admin.register(Indicateur)
class IndicateurAdmin(admin.ModelAdmin):
    list_display = ('label', 'sous_composant', 'created')



@admin.register(CategorieDepense)
class CategorieDepenseAdmin(admin.ModelAdmin):
    list_display = ('label',) # Affiche le champ 'label' dans la liste des catégories


@admin.register(TypeUnite)
class TypeUniteAdmin(admin.ModelAdmin):
    list_display = ('label',) # Affiche le champ 'label' dans la liste des types d'unités


@admin.register(TypeProcedureAcquisition)
class TypeProcedureAcquisitionAdmin(admin.ModelAdmin):
    list_display = ('label',) # Affiche le champ 'label' dans la liste des types de procédures


@admin.register(Decaissement)
class DecaissementAdmin(admin.ModelAdmin):
    list_display = ('tache','montant', 'status', 'in_drf', 'order', 'created', 'modified') # Affiche les champs spécifiés
    list_filter = ('status', 'in_drf') # Ajoute des filtres pour 'status' et 'in_drf'
    search_fields = ('pk', 'montant') # Ajoute une barre de recherche pour le pk et le montant
    date_hierarchy = 'created' # Permet de naviguer par date de création


@admin.register(TypeUGP)
class TypeUGPAdmin(admin.ModelAdmin):
    list_display = ('label',)







