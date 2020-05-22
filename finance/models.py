from django.db import models
from events.models import Event
from django.core import validators
from django.utils.html import format_html
import django
from django.utils.text import slugify


class Ticket(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    SINGLE_ADULT = 1
    CHILD = 2
    FAMILY = 3
    OAP = 4
    STUDENT = 5
    TICKET_TYPES = (
        (SINGLE_ADULT, ('Adult aged 16 - 65')),
        (CHILD, ('Child aged 3 - 15')),
        (FAMILY, ('Up to 2 Adults, 2 - 3 children')),
        (OAP, ('Over 65')),
        (STUDENT, ('Over 16, under 25 and in full time education'))
    )

    price = models.DecimalField(max_digits=6, decimal_places=2)
    ticket_type = models.CharField(max_length=12, choices=TICKET_TYPES, default=1)
    ticket_quantity = models.IntegerField(default=1)
    slug = models.SlugField(unique=True, editable=False, max_length=80, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.event.title)
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, {}, {}'.format(self.price, self.ticket_type, self.ticket_quantity)

    def get_event(self):
        return self.event.title

    class Meta:
        ordering = ['ticket_type']


class Merchandise(models.Model):

    merchandise_name = models.CharField(max_length=100, blank=False, validators=[validators.RegexValidator(
            regex='^[0-9A-Za-z ]*$', message="Alphanumeric only for merchandise name", code="invalid merchandise_name")])
    stock_number = models.CharField(max_length=10, blank=False, validators=[validators.RegexValidator(
            regex='^[0-9A-Z]*$', message="Alphanumeric only stock_number", code="invalid stock_number")])
    merchandise_description = models.CharField(max_length=250, blank=True, validators=[validators.RegexValidator(
            regex='^[0-9A-Za-z ]*$', message="Alphanumeric only merchandise_description", code="invalid merchandise_description")])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    merchandise_quantity = models.IntegerField(default=1)
    slug = models.SlugField(unique=True, editable=False, max_length=merchandise_name.max_length, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.merchandise_name)
        super(Merchandise, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.merchandise_name, self.stock_number)

    class Meta:
        ordering = ['merchandise_name']


class Giftaid(models.Model):

    name = models.CharField(max_length=50, blank=True, validators=[validators.RegexValidator(
        regex='^[A-Za-z ]*$', message="Alpha only for name", code="invalid campaign")])
    first_line_address = models.CharField(max_length=250, blank=True, validators=[validators.RegexValidator(
        regex='^[0-9A-Za-z ]*$', message="Alphanumeric only for first_line_address",
        code="invalid first_line_address")])
    city = models.CharField(max_length=100, blank=False, validators=[validators.RegexValidator(
        regex='^[A-Za-z ]*$', message="Alphanumeric only for city", code="invalid city")])
    postcode = models.CharField(max_length=8, blank=False, validators=[validators.RegexValidator(
        regex='^[0-9A-Z ]*$', message="Capital Alphanumeric only for postcode", code="invalid postcode")])
    country = models.CharField(max_length=100, blank=False, validators=[validators.RegexValidator(
        regex='^[A-Za-z ]*$', message="Alphanumeric only for country", code="invalid country")])
    phone_number = models.CharField(max_length=17, validators=[validators.RegexValidator(
        regex='^\+?1?\d{9,15}$', message="Phone number must be digits only, up to 15 digits allowed",
        code="invalid event in phone_number")])
    slug = models.SlugField(unique=True, editable=False, max_length=name.max_length, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Giftaid, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['name']


class Donation(models.Model):

    campaign = models.CharField(max_length=100, blank=False, validators=[validators.RegexValidator(
            regex='^[0-9A-Za-z ]*$', message="Alphanumeric only for campaign", code="invalid campaign")])
    target = models.DecimalField(max_digits=6, decimal_places=2)
    amount_2_donate = models.DecimalField(max_digits=6, decimal_places=2)
    giftaid = models.BooleanField(default=False)
    giftaid_detail = models.ForeignKey(Giftaid, null=True, default=None, blank=True, on_delete=models.CASCADE)
    donation_quantity = models.IntegerField(default=1)
    slug = models.SlugField(unique=True, editable=False, max_length=200, default=None)

    def save(self, *args, **kwargs):
        slug_string = self.campaign + ' ' + self.giftaid_detail.name
        self.slug = slugify(slug_string)
        super(Donation, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.amount_2_donate, self.giftaid_detail.name)

    class Meta:
        ordering = ['campaign']


class Basket(models.Model):

    basket_id = models.CharField(max_length=10, blank=False, default="XXXXXXX", validators=[validators.RegexValidator(
            regex='^[0-9A-Z]*$', message="Alphanumeric only basket_it", code="invalid basket_id")])
    date = models.DateTimeField(default=django.utils.timezone.now)
    ticket = models.ManyToManyField(Ticket)
    donation = models.ManyToManyField(Donation)
    merchandise = models.ManyToManyField(Merchandise)
    paid = models.BooleanField(default=False)
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, default=00000)
    slug = models.SlugField(unique=True, editable=False, max_length=basket_id.max_length, default=None)
    #todo integrate a payment gateway once basket working wel

    def save(self, *args, **kwargs):
        self.slug = slugify(self.basket_id)
        super(Basket, self).save(*args, **kwargs)

    def list_basket_contents(self):
        """Return a list of items in basket"""
        ret_str = ''
        for items in Basket.objects.all():
            ret_str += '<ul> {} </ul> '.format(items)
        return format_html(ret_str)

    def get_total_cost(self):
        """sum the total cost of items in the basket"""
        total_price = 0
        if len(list(Basket.objects.all())) > 0:
            for items in Basket.objects.all():
                total_price += items.ticket.price
                total_price += items.merchandise.price
                total_price += items.donation.amount_2_donate
            return total_price
        else:
            return total_price

    def __str__(self):
        return '{}'.format(self.basket_id)

