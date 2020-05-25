from django import forms
from .models import Role, Person, Staff, Volunteer, Working_Hrs


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'role_responsibility', 'responsible_4_roles']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['userid', 'email', 'phone_number', 'first_name', 'second_name', 'date_of_birth', 'postcode', 'address',
                  'organisation_role', 'allowed_access', 'notes', 'line_manage']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['person', 'staff_number', 'nat_insurance_num', 'salary', 'hours']


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['person', 'staff_number', 'hours']


class WorkingHoursForm(forms.ModelForm):
    class Meta:
        model = Working_Hrs
        fields = ['day_of_week', 'start', 'end', 'duration']
