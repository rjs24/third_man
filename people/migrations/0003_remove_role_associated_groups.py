# Generated by Django 3.0.3 on 2020-05-24 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20200522_2123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='associated_groups',
        ),
    ]
