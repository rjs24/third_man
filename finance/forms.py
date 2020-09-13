from django import forms
from .models import Ticket, Donation, Merchandise, Basket, Giftaid


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_number', 'event', 'price', 'ticket_type', 'ticket_quantity']


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['campaign', 'target', 'amount_2_donate', 'giftaid', 'giftaid_detail', 'donation_quantity']


class MerchandiseForm(forms.ModelForm):
    class Meta:
        model = Merchandise
        fields = ['merchandise_name', 'stock_number', 'merchandise_description', 'price', 'merchandise_quantity']


class GiftaidForm(forms.ModelForm):
    class Meta:
        model = Giftaid
        fields = ['name', 'first_line_address', 'city', 'postcode', 'country', 'phone_number']


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['basket_id', 'date', 'ticket', 'donation', 'merchandise', 'paid', 'total_cost']