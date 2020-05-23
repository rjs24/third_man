from django.db import models
from django.core import validators
from datetime import timedelta
import django
from django.utils.html import format_html
from django.utils.text import slugify
from people.models import Person


class Event(models.Model):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4
    RECURRENCE_INTERVAL = (
        (DAILY, ('Set event to daily recurrence')),
        (WEEKLY, ('Set event to weekly recurrence')),
        (MONTHLY, ('Set event to monthly recurrence')),
        (YEARLY, ('Set event to yearly recurrence')),
    )

    event_owner = models.ForeignKey('people.Person', on_delete=models.CASCADE, related_name='event_owners_set', null=True)
    title = models.CharField(max_length=80, null=False, blank=False, primary_key=True, validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9 ]*$', message="Event title must be alphanumeric", code="invalid event title")])
    start = models.DateTimeField(default=django.utils.timezone.now)
    end = models.DateTimeField(default=django.utils.timezone.now)
    duration = models.DurationField(default=timedelta())
    invites = models.ManyToManyField('comms.CommsGroup')
    recurring = models.BooleanField(default=False)
    description = models.TextField(max_length=150, default='', validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9 .,\r\n]*$', message="Only use alphanumerics please", code="invalid event description")])
    website_publish = models.BooleanField(default=False)
    recurrence_interval = models.PositiveSmallIntegerField(choices=RECURRENCE_INTERVAL, default=WEEKLY)
    slug = models.SlugField(unique=True, editable=False, max_length=title.max_length, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.title, self.event_owner)

    def list_group_names(self):
        """Return a list of CommsGroups in invites"""
        ret_str = ''
        for inv in self.invites.all():
            ret_str += '<ul> {} </ul> '.format(inv)
        return format_html(ret_str)

    class Meta:
        ordering = ['start']
