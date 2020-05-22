from django.contrib import admin
from .models import Role, Person, Staff, Working_Hrs, Volunteer


class role_admin_inline(admin.TabularInline):
    model = Role
    extra = len(list(Role.objects.all()))


class RoleAdmin(admin.ModelAdmin):

    model = Role
    list_display = ('role_name', 'role_responsibility', 'group_names', 'responsible_roles')
    inline = (role_admin_inline,)

    def group_names(self, obj):
        return obj.list_group_names()

    def responsible_roles(self, obj):
        return obj.get_responsible_roles()


class PersonAdmin(admin.ModelAdmin):

    model = Person
    list_display = ('userid', 'phone_number', 'first_name', 'second_name', 'date_of_birth', 'postcode', 'address',
                     'role_name', 'allowed_access')

    def role_name(self, obj):
        return obj.return_organisational_role


class Working_HrsAdmin(admin.ModelAdmin):

    model = Working_Hrs
    list_display = ('start', 'end', 'duration')


class StaffAdmin(admin.ModelAdmin):

    model = Staff
    list_display = ('get_personid', 'staff_number', 'nat_insurance_num', 'salary', 'get_working_hrs')

    def get_personid(self, obj):
        return obj.return_personid

    def get_working_hrs(self, obj):
        return obj.list_working_hrs


class VolunteerAdmin(admin.ModelAdmin):

    model = Volunteer
    list_display =  ('get_personid', 'staff_number', 'get_working_hrs')

    def get_personid(self, obj):
        return obj.return_personid

    def get_working_hrs(self, obj):
        return obj.Working_Hrs.list_working_hrs


admin.site.register(Role, RoleAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Working_Hrs, Working_HrsAdmin)
