from django import forms
from .models import Vehicule, EmpruntVehicule

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = '__all__'
        widgets = {
            'entretients': forms.SelectMultiple(choices=[
                "Vidange d’huile",
                "Lubrification du châssis",
                "Changement du filtre à huile",
                "Changement du filtre à air",
                "Vidange du liquide de transmission",
                "Rinçage du système de refroidissement",
                "Alignement des roues",
                "Remplacement des pneumatiques",
                "Réglage des freins",
                "Réglage moteur" ,
                "Autre service",
            ]),
        }

    def clean(self):
        cleaned_data = super().clean()
        entretients = cleaned_data.get('entretients')

        # Logique pour mettre à jour le champ entretients
        if entretients:
            # Exemple de mise à jour : ajouter un entretien par défaut
            if 'default_entretien' not in entretients:
                entretients.append('default_entretien')

        cleaned_data['entretients'] = entretients
        return cleaned_data



class EmpruntVehiculeForm(forms.ModelForm):
    km_out = forms.IntegerField(label="Kilometrage de sortie")
    km_in = forms.IntegerField(label="Kilometrage de retour", required=False)

    class Meta:
        model = EmpruntVehicule
        fields = '__all__'
        widgets = {
            'date_sortie': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_retour': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'mission': forms.Textarea(attrs={'rows': 4}),
        }