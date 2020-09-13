from rest_framework.routers import DefaultRouter
from .views.ticket_views import APITicketViewSet
from .views.donation_views import APIDonationViewSet
from .views.merchandise_views import APIMerchandiseViewSet
from .views.giftaid_views import APIGiftaidViewSet
from .views.basket_views import APIBasketViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'finance/ticket', APITicketViewSet, basename='ticket-list')
router.register(r'finance/ticket/(?P<slug>[-\w\d]+)/$', APITicketViewSet, basename='ticket-detail')
router.register(r'finance/donation', APIDonationViewSet, basename='donation-list')
router.register(r'finance/donation/(?P<slug>[-\w\d]+)/$', APIDonationViewSet, basename='donation-detail')
router.register(r'finance/merchandise', APIMerchandiseViewSet, basename='merchandise-list')
router.register(r'finance/merchandise/(?P<slug>[-\w\d]+)/$', APIMerchandiseViewSet, basename='merchandise-detail')
router.register(r'finance/giftaid', APIGiftaidViewSet, basename='giftaid-list')
router.register(r'finance/giftaid/(?P<slug>[-\w\d]+)/$', APIGiftaidViewSet, basename='giftaid-detail')
router.register(r'finance/basket', APIBasketViewSet, basename='basket-list')
router.register(r'finance/basket/(?P<slug>[-\w\d]+)/$', APIBasketViewSet, basename='basket-detail')