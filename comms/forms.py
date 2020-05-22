from django import forms
from .models import CommsGroup


class CommsForm(forms.ModelForm):
    class Meta:
        model = CommsGroup
        fields = ['group_name', 'group_owner', 'group_purpose', 'group_membership']