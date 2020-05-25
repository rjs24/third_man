from rest_framework import serializers
from .models import Event
from comms.serializers import CommsGroupSerializer
from comms.models import CommsGroup
from people.serializers import PersonSerializer


class EventSerializer(serializers.ModelSerializer):

    invites = CommsGroupSerializer(many=True)
    event_owner = PersonSerializer(many=False, read_only=True)

    # invites_comms = serializers.CharField(source='commsgroup.group_name', read_only=True)
    # event_owner = serializers.CharField(source='person.pk', read_only=True)
    class Meta:
        model = Event
        fields = ['event_owner', 'title', 'start', 'end', 'duration', 'invites', 'recurring', 'description',
                  'website_publish', 'recurrence_interval']
        depth = 3

    def create(self, validated_data):
        print(validated_data)
        comms_grp_data = validated_data.pop('invites')
        print(comms_grp_data)
        event = Event.objects.create(**validated_data)
        for grps in comms_grp_data:
            grps, created = CommsGroup.objects.get_or_create(group_name=grps['group_name'])
            event.invites.add(grps)
        return event