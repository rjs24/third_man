from rest_framework import serializers
from .models import CommsGroup


class CommsGroupSerializer(serializers.ModelSerializer):

    grp_membership = serializers.RelatedField(source='person.userid', read_only=True)
    class Meta:
        model = CommsGroup
        fields = ['group_name', 'group_owner', 'group_purpose', 'grp_membership','slug']
