from typing import override
from django import forms

from rapportage.models import Rapport


class RapportForm(forms.ModelForm):

    class Meta:
        model = Rapport
        required = ('file','label')
        exclude = ('user','state','type','status')

    @override
    def save(self, commit=True):
        rapport = super().save(commit)
        # attacher les roles et departements
        def attach_roles_and_departements(rapport, commit):
            rapport.roles.set(self.cleaned_data['roles'])
            rapport.departements.set(self.cleaned_data['departements'])
        
        if commit:
            rapport.save()
            attach_roles_and_departements(rapport, commit)
        return rapport

