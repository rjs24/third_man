from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_owner', 'title', 'start', 'end', 'invites', 'description', 'website_publish',
                  'recurrence_interval']
