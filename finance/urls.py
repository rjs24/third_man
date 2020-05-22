from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include


router = DefaultRouter()

router.register(r'api/ticket', views.TicketViewSet, 'Ticket')
router.register(r'api/merchandise', views.MerchandiseViewSet, 'Merchandise')
router.register(r'api/giftaid', views.GiftaidViewSet, 'Giftaid')
router.register(r'api/donation', views.DonationViewSet, 'Donation')
router.register(r'api/basket', views.BasketViewSet, 'Basket')

urlpatterns = router.urls

app_name = 'finance'
urlpatterns = [
    path(r'', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
