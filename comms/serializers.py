from rest_framework import serializers
from .models import CommsGroup


class CommsGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommsGroup
        fields = '__all__'
