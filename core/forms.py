from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User, Role


class UserCreationWithRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label="Rôle")

    class Meta:
        model = User
        fields = ['username', 'email','last_name','first_name', 'contact', 'role', 'departement', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }