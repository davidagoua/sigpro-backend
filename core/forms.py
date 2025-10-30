from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User, Role, Exercice
from planification.models import Drf



class BootstrapForm(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Gestion des différents types de champs
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'

            # Ajouter un placeholder si nécessaire
            if not field.help_text and field.label:
                field.widget.attrs['placeholder'] = field.label


class UserCreationWithRoleForm(BootstrapForm,forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="Rôle")

    class Meta:
        model = User
        fields = ['username', 'email','last_name','first_name', 'contact', 'role', 'departement', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ExerciceForm(forms.ModelForm):
    date_debut = forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    date_fin = forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Exercice
        exclude = ['status']
        attrs = {'class': 'form-control'}


class DrfForm(BootstrapForm, forms.ModelForm):
    date = forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    label = forms.CharField(label="Numero de la DRF")
    class Meta:
        model = Drf
        exclude = ['exercice']