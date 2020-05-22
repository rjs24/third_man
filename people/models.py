from django.contrib.auth.models import User
from django.db import models
from django.core import validators
import django
from datetime import timedelta
from django.utils.html import format_html
from django.utils.text import slugify


class Role(models.Model):
    role_name = models.CharField(max_length=25, primary_key=True, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z ]*$', message="Please use alphanumeric only",
        code="invalid event in role_name")])
    role_responsibility = models.TextField(max_length=500, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z, .]*$', message="Please use alphanumeric only",
        code="invalid event in role_responsibility")])
    associated_groups = models.ManyToManyField('comms.CommsGroup', blank=True, default=None)
    responsible_4_roles = models.ManyToManyField("self", blank=True, default=None, related_name='responsible_roles',
                                                 symmetrical=False)
    slug = models.SlugField(unique=True, editable=False, max_length=role_name.max_length, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.role_name)
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.role_name)

    def list_group_names(self):
        """Return a list of commsGroup names"""
        ret_grp = ''
        for grps in self.associated_groups.all():
            ret_grp += '<ul> {} </ul> '.format(grps)
        return format_html(ret_grp)

    def get_responsible_roles(self):
        """return a list of roles"""
        ret_rol = ''
        for rols in self.responsible_4_roles.all():
            if rols.role_name == self.role_name:
                continue
            else:
                ret_rol += '<ul> {} </ul> '.format(rols)
        return format_html(ret_rol)

    class Meta:
        ordering = ['role_name']


class Person(models.Model):

    PRIVATE = 1
    PROTECTED = 2
    PUBLIC = 3
    ACCESS_LEVEL = (
        (PRIVATE, ('May create private events only or defined individuals/groups')),
        (PROTECTED, ('May create events that are open to anyone within organisation')),
        (PUBLIC, ('May create events that are open to anyone, including public and autopublish to website'))
    )

    userid = models.ForeignKey(User, on_delete=models.PROTECT)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=17,validators=[validators.RegexValidator(
        regex='^\+?1?\d{9,15}$', message="Phone number must be digits only, up to 15 digits allowed",
        code="invalid event in phone_number")])
    first_name = models.CharField(max_length=50,validators=[validators.RegexValidator(
        regex='^[a-zA-Z]*$', message="First name must be alpha characters only",
        code="invalid event in first_name")])
    second_name = models.CharField(max_length=50,validators=[validators.RegexValidator(
        regex='^[a-zA-Z-]*$', message="Surname must be alpha characters only",
        code="invalid event in second_name")])
    date_of_birth = models.DateField()
    postcode = models.CharField(max_length=8,validators=[validators.RegexValidator(
        regex='^[A-Z0-9]*$', message="Postcode can only be alphanumeric upper-case",
        code="invalid event in postcode")])
    address = models.TextField(max_length=150, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z, \r\n]*$', message="Please use alphanumeric only",
        code="invalid event in address")])
    organisation_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    allowed_access = models.PositiveSmallIntegerField(choices=ACCESS_LEVEL, default=PRIVATE)
    notes = models.TextField(max_length=500, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z, .\r\n]*$', message="Please use alphanumeric only",
        code="invalid event in notes")])
    line_manage = models.ForeignKey(Role, default="None", related_name='manages_table', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, editable=False, max_length=50, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.userid)
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.second_name)

    def return_organisational_role(self):
        """Return foreign key organisational_role"""
        return self.organisation_role.role_name

    def list_key_person_atts(self):
        """Return a list of userid's for commsGroup"""
        return format_html(
            '<span style="color: #000000{}:" {}, {}</span>',
            self.userid, self.email, self.phone_number
        )

    class Meta:
        ordering = ['userid']


class Working_Hrs(models.Model):

    DAYS = [
        (1, ("Monday")),
        (2, ("Tuesday")),
        (3, ("Wednesday")),
        (4, ("Thursday")),
        (5, ("Friday")),
        (6, ("Saturday")),
        (7, ("Sunday"))
    ]

    day_of_week = models.PositiveSmallIntegerField(choices=DAYS, default=1)
    start = models.TimeField(default=django.utils.timezone.now)
    end = models.TimeField(default=django.utils.timezone.now)
    duration = models.DurationField(default=timedelta())

    def __str__(self):
        return '{}: {} -> {}'.format(self.day_of_week, self.start, self.end)

    class Meta:
        ordering = ['start']


class Staff(models.Model):

    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    staff_number = models.CharField(max_length=5, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z]*$', message="Please use alphanumeric only",
        code="invalid event in staff_number")])
    nat_insurance_num = models.CharField(max_length=12, validators=[validators.RegexValidator(
        regex='^[A-Z0-9 ]*$', message="Please use capital alphanumeric only",
        code="invalid event in nat_insurance_num")])
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    hours = models.ManyToManyField(Working_Hrs)
    slug = models.SlugField(unique=True, editable=False, max_length=staff_number.max_length, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.staff_number)
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return '{},{}'.format(self.person, self.staff_number)

    def return_personid(self):
        """Get person userid back to admin"""
        return self.person.userid

    def list_working_hrs(self):
        """Return a list of working hrs"""
        wks_hrs = ''
        for hrs in self.hours.all():
            wks_hrs +=  '<ul> {} </ul> '.format(hrs)
        return format_html(wks_hrs)

    class Meta:
        ordering = ['person']


class Volunteer(models.Model):

    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    staff_number = models.CharField(max_length=5, validators=[validators.RegexValidator(
        regex='^[A-Z0-9a-z]*$', message="Please use alphanumeric only",
        code="invalid event in staff_number")])
    hours = models.ManyToManyField(Working_Hrs)
    slug = models.SlugField(unique=True, editable=False, max_length=staff_number.max_length, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.staff_number)
        super(Volunteer, self).save(*args, **kwargs)

    def __str__(self):
        return '{},{}'.format(self.person, self.staff_number)

    def return_personid(self):
        """Get person userid back to admin"""
        return self.person.userid

    def list_working_hrs(self):
        """Return a list of working hrs"""
        wks_hrs = ''
        for hrs in self.hours.all():
            wks_hrs +=  '<ul> {} </ul> '.format(hrs)
        return format_html(wks_hrs)


    class Meta:
        ordering = ['person']







