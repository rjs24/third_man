from django.db import models
from django.core import validators
from django.utils.html import format_html
from django.utils.text import slugify


class CommsGroup(models.Model):
    group_owner = models.ForeignKey('people.Person', on_delete=models.CASCADE, related_name='group_owners_set')
    group_name = models.CharField(max_length=50, primary_key=True, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z ]*$', message="Please use alphanumeric only",
        code="invalid event in group_name")])
    group_purpose = models.TextField(max_length=150, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z, ]*$', message="Please use alphanumeric only",
        code="invalid event in group_purpose")])
    group_membership = models.ManyToManyField('people.Person', blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=group_name.max_length, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super(CommsGroup, self).save(*args, **kwargs)
        self.group_membership.add(self.group_owner)
        return self

    def __str__(self):
        return '{}'.format(self.group_name)

    def list_group_names(self):
        """Return a list of group_names"""
        ret_str = ''
        for peeps in self.group_membership.all():
            ret_str += '<ul> {} </ul> '.format(peeps)
        return format_html(ret_str)

    class Meta:
        ordering = ['group_name']

