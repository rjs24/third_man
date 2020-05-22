from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, Person, Working_Hrs, Staff, Volunteer

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    associated_groups = serializers.RelatedField(source='commsgroup', read_only=True)
    class Meta:
        model = Role
        fields = ['role_name', 'role_responsibility', 'assoicated_groups', 'responsible_4_roles']


class PersonSerializer(serializers.ModelSerializer):

    userid = serializers.RelatedField(source='person', read_only=True)
    organisation_role = serializers.RelatedField(source='role', read_only=True)
    line_manage = serializers.RelatedField(source='role', read_only=True)

    class Meta:
        model = Person
        fields = ['userid', 'email', 'phone_number', 'first_name', 'second_name', 'data_of_birth', 'postcode', 'address',
                  'organisation_role', 'allowed_access', 'notes', 'line_manage']


class Working_HrsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Working_Hrs
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):

    person = serializers.RelatedField(source='person', read_only=True)
    hours = serializers.RelatedField(source='working_hrs', read_only=True)
    class Meta:
        model = Staff
        fields = ['person', 'staff_number', 'nat_insurance_num', 'salary', 'hours']


class VolunteerSerializer(serializers.ModelSerializer):

    person = serializers.RelatedField(source='person', read_only=True)
    hours = serializers.RelatedField(source='working_hrs', read_only=True)
    class Meta:
        model = Volunteer
        fields = fields = ['person', 'staff_number', 'hours']
