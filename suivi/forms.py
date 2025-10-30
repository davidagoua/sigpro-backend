from django import forms

from core.forms import BootstrapForm
from planification.models import Drf, Decaissement
from suivi.models import CommentaireTDR


class CancelTDRForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CommentaireTDR
        fields = ('comment',)


class CancelTDRProgrammeForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CommentaireTDR
        fields = ('comment',)




class DecaisementForm(BootstrapForm, forms.ModelForm):
    motif = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}), label="Motifs de décaissement")
    class Meta:
        model = Decaissement
        fields = ['montant','motif']