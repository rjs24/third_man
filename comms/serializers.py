from rest_framework import serializers
from .models import CommsGroup


class CommsGroupSerializer(serializers.ModelSerializer):

    group_membership = serializers.RelatedField(source='person', read_only=True)
    class Meta:
        model = CommsGroup
        fields = ['group_name', 'group_owner', 'group_purpose', 'group_membership','slug']
