from rest_framework import serializers
from .models import CommsGroup
from people.serializers import PersonSerializer
from people.models import Person


class CommsGroupSerializer(serializers.ModelSerializer):

    #group_membership = serializers.RelatedField(source='person', read_only=True)
    group_membership = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = CommsGroup
        fields = ['group_name', 'group_owner', 'group_purpose', 'group_membership','slug']
