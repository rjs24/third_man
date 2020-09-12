from django.contrib import admin
from .models import Ticket, Donation, Merchandise, Basket, Giftaid


class TicketAdmin(admin.ModelAdmin):

    model = Ticket
    list_display = ('events', 'price', 'ticket_type', 'ticket_quantity')

    def events(self, obj):
        return obj.get_event


class MerchandiseAdmin(admin.ModelAdmin):

    model = Merchandise
    list_display = ('merchandise_name', 'stock_number', 'merchandise_description', 'price', 'merchandise_quantity')


class DonationAdmin(admin.ModelAdmin):

    model = Donation
    list_display = ('campaign', 'target', 'amount_2_donate', 'giftaid', 'donation_quantity')


class GiftaidAdmin(admin.ModelAdmin):

    model = Giftaid
    list_display = ('name','first_line_address', 'city', 'postcode', 'country', 'phone_number')


class BasketAdmin(admin.ModelAdmin):

    model = Basket
    list_display = ('basket_contents',)

    def basket_contents(self, obj):
        return obj.list_all_baskets


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Giftaid, GiftaidAdmin)