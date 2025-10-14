from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User, Role, Exercice


class UserCreationWithRoleForm(forms.ModelForm):
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