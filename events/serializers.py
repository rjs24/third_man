from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    invite_comms = serializers.RelatedField(source='commsgroup.group_name', read_only=True)
    event_owner = serializers.RelatedField(source='person.userid', read_only=True)
    class Meta:
        model = Event
        fields = ['event_owner', 'title', 'start', 'end', 'duration', 'invite_comms', 'recurring', 'description',
                  'website_publish', 'recurrence_interval']
