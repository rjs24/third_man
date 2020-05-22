from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, MerchandiseViewSet, GiftaidViewSet, DonationViewSet, BasketViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'tickets', TicketViewSet, basename='Tickets-list')
router.register(r'tickets_detail', TicketViewSet, basename='Tickets-detail')
router.register(r'merchandise', MerchandiseViewSet, basename='Merchandise-list')
router.register(r'merchandise_detail', MerchandiseViewSet, basename='Merchandise-detail')
router.register(r'giftaid', GiftaidViewSet, basename='Giftaid-list')
router.register(r'giftaaid_detail', TicketViewSet, basename='Giftaid-detail')
router.register(r'donation', DonationViewSet, basename='Donations-list')
router.register(r'donation_detail', DonationViewSet, basename='Donations-detail')
router.register(r'basket', BasketViewSet, basename='Basket-list')
router.register(r'basket_detail', BasketViewSet, basename='Basket-detail')
