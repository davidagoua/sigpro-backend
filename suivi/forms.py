from django import forms

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