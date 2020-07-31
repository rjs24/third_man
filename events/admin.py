from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('title', 'event_owner', 'start', 'end', 'duration', 'invites', 'description', 'recurrence_interval',
                    'website_publish')


    def invites(self, obj):
        return obj.list_group_names


admin.site.register(Event, EventAdmin)
