# Generated by Django 3.0.7 on 2020-09-06 21:13

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comms', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('title', models.CharField(max_length=80, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(code='invalid event title', message='Event title must be alphanumeric', regex='^[a-zA-Z0-9 ]*$')])),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration', models.DurationField(default=datetime.timedelta(0))),
                ('description', models.TextField(default='', max_length=150, validators=[django.core.validators.RegexValidator(code='invalid event description', message='Only use alphanumerics please', regex='^[a-zA-Z0-9 .,\r\n]*$')])),
                ('website_publish', models.BooleanField(default=False)),
                ('recurrence_interval', models.PositiveSmallIntegerField(choices=[(0, 'Set event to non-recurring'), (1, 'Set event to daily recurrence'), (2, 'Set event to weekly recurrence'), (3, 'Set event to monthly recurrence'), (4, 'Set event to yearly recurrence')], default=2)),
                ('slug', models.SlugField(default=None, max_length=80, unique=True)),
                ('event_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_owners_set', to='people.Person')),
                ('invites', models.ManyToManyField(to='comms.CommsGroup')),
            ],
            options={
                'ordering': ['start'],
            },
        ),
    ]
