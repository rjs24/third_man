from rest_framework.serializers import ModelSerializer
from .models import Ticket, Merchandise, Giftaid, Donation, Basket


class TicketSerializer(ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'


class MerchandiseSerializer(ModelSerializer):

    class Meta:
        model = Merchandise
        fields = '__all__'


class GiftaidSerializer(ModelSerializer):

    class Meta:
        model = Giftaid
        fields = '__all__'


class DonationSerializer(ModelSerializer):
    giftaid_detail = GiftaidSerializer(many=False, read_only=True)

    class Meta:
        model = Donation
        fields = ['campaign', 'target', 'amount_2_donate', 'giftaid', 'giftaid_detail', 'donation_quantity']


class BasketSerializer(ModelSerializer):
    ticket = TicketSerializer(many=True, read_only=True)
    donation = DonationSerializer(many=True, read_only=True)
    merchandise = MerchandiseSerializer(many=True, read_only=True)
    class Meta:
        model = Basket
        fields = ['basket_id', 'date', 'ticket', 'donation', 'merchandise', 'paid', 'total_cost']