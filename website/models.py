from django.db import models
from events.models import Event
from django.core.validators import RegexValidator

class PublicEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    more_info_link = models.URLField(max_length=250)
    ticket_link =  models.URLField(max_length=250)
    contact_number = models.CharField(validators=[RegexValidator(regex='^\+?1?\d{9,15}$', message="Enter number in valid format only")],
                                      max_length=17, blank=True)
    twitter_link = models.URLField(max_length=250)
    facebook_link = models.URLField(max_length=250)
    linked_organisation = models.URLField(max_length=250)

    def return_event_title(self):
        return self.event.title

    def __str__(self):
        return '{},{},{},{},{}.{},{}'.format(self.event, self.more_info_link, self.ticket_link, self.contact_number,
                                             self.twitter_link, self.facebook_link, self.linked_organisation)
    class Meta:
        ordering = ['event']
