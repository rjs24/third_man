from django.contrib import admin
from .models import CommsGroup


class CommsAdmin(admin.ModelAdmin):
    model = CommsGroup
    list_display = ('group_name', 'group_purpose', 'group_list_membership')

    def group_list_membership(self, obj):
        return obj.list_group_names()


admin.site.register(CommsGroup, CommsAdmin)
