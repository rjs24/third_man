from django.contrib import admin
from .models import PublicEvent
from events.models import Event

class PublicEventAdmin(admin.ModelAdmin):

    model = PublicEvent
    list_display = ('get_event_title', 'more_info_link', 'ticket_link', 'contact_number', 'twitter_link', 'facebook_link',
                    'linked_organisation')

    def get_event_title(self, obj):
        return obj.return_event_title


admin.site.register(PublicEvent, PublicEventAdmin)