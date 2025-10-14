from django import forms
from django.forms import inlineformset_factory

from .models import  Tache, Decaissement




class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        exclude = ['status','user','departement','montant_engage','depends_on']  # Ou spécifier les champs explicitement
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'depends_on': forms.SelectMultiple(attrs={'class': 'select2'}), #Utilise select2 si installé
        }
        labels = {
            'label': 'Libellé de la tâche',
            'categorie': 'Catégorie de dépense',
            'indicateur': 'Indicateur associé',
            'unite': 'Unité de mesure',
            'montant_engage': 'Montant engagé (FCFA)',
            'cout': 'Coût unitaire (FCFA)',
            'quantite': 'Quantité',
            'ugp': 'Unité de gestion de projet',
            'date_debut': 'Date de début',
            'date_fin': 'Date de fin',
            'responsable': 'Nom du responsable',
            'depends_on': 'Tâches dépendantes',
        }
        help_texts = {
            'montant_engage': 'Le montant total alloué à cette tâche.',
            'cout': 'Le coût unitaire pour une unité de la tâche.',
            'quantite': 'Le nombre d\'unités de la tâche.',
            'depends_on': 'Sélectionnez les tâches qui doivent être terminées avant celle-ci.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['label'].widget.attrs.update({'class': 'form-control'})
        self.fields['categorie'].widget.attrs.update({'class': 'form-control'})
        self.fields['indicateur'].widget.attrs.update({'class': 'form-control'})
        self.fields['unite'].widget.attrs.update({'class': 'form-control'})
        self.fields['ugp'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsable'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin and date_debut > date_fin:
            raise forms.ValidationError("La date de début doit être antérieure à la date de fin.")

        quantite = cleaned_data.get('quantite')
        cout = cleaned_data.get('cout')
        montant_engage = cleaned_data.get('montant_engage')

        if quantite is not None and cout is not None and montant_engage is not None:
            if quantite * cout > montant_engage:
                raise forms.ValidationError("Le montant engagé doit être supérieur ou égal au coût total (quantité * coût unitaire).")

        return cleaned_data


class UpdateTacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        exclude = ['type', 'indicateur', 'depends_on', 'status_validation', 'status_execution',
                   'status']  # Ou spécifier les champs explicitement
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'depends_on': forms.SelectMultiple(attrs={'class': 'select2'}),  # Utilise select2 si installé
        }
        labels = {
            'label': 'Libellé de la tâche',
            'categorie': 'Catégorie de dépense',
            'indicateur': 'Indicateur associé',
            'unite': 'Unité de mesure',
            'montant_engage': 'Montant engagé (FCFA)',
            'cout': 'Coût unitaire (FCFA)',
            'quantite': 'Quantité',
            'ugp': 'Unité de gestion de projet',
            'date_debut': 'Date de début',
            'date_fin': 'Date de fin',
            'responsable': 'Nom du responsable',
            'depends_on': 'Tâches dépendantes',
            'planificationcout_set': 'Planifications des coûts',
        }
        help_texts = {
            'montant_engage': 'Le montant total alloué à cette tâche.',
            'cout': 'Le coût unitaire pour une unité de la tâche.',
            'quantite': 'Le nombre d\'unités de la tâche.',
            'depends_on': 'Sélectionnez les tâches qui doivent être terminées avant celle-ci.',
            'planificationcout_set': 'Sélectionnez ou ajoutez des planifications de coûts liées à cette tâche.',
        }


class DecaissementForm(forms.ModelForm):
    class Meta:
        model = Decaissement
        fields = ['montant', 'in_drf',]


DecaissementFormSet = inlineformset_factory(
    Tache,
    Decaissement,
    form=DecaissementForm,
    extra=1,  # Nombre de formulaires vides à afficher
    can_delete=True,
)