from django.conf.urls import url, include
from .views.ticket_views import TicketFormView, TicketDeleteConfirmView, TicketViewSet
from .views.merchandise_views import MerchandiseFormView, MerchandiseDeleteConfirmView, MerchandiseViewSet
from .views.giftaid_views import GiftaidFormView, GiftaidDeleteConfirmView, GiftaidViewSet
from .views.donation_views import DonationFormView, DonationDeleteConfirmView, DonationViewSet
from .views.basket_views import BasketFormView, BasketDeleteConfirmView, BasketViewSet
from .api import router


ticket_list = TicketViewSet.as_view({
    'get':'list',
    'post':'create',
})

ticket_record = TicketViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

ticket_delete = TicketViewSet.as_view({
    'post':'destroy'
})

merchandise_list = MerchandiseViewSet.as_view({
    'get':'list',
    'post':'create',
})

merchandise_record = MerchandiseViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

merchandise_delete = MerchandiseViewSet.as_view({
    'post':'destroy'
})

giftaid_list = GiftaidViewSet.as_view({
    'get':'list',
    'post':'create',
})

giftaid_record = GiftaidViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

giftaid_delete = GiftaidViewSet.as_view({
    'post':'destroy'
})

donation_list = DonationViewSet.as_view({
    'get':'list',
    'post':'create',
})

donation_record = DonationViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

donation_delete = DonationViewSet.as_view({
    'post':'destroy'
})

basket_list = BasketViewSet.as_view({
    'get':'list',
    'post':'create',
})

basket_record = BasketViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

basket_delete = BasketViewSet.as_view({
    'post':'destroy'
})

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^finance/ticket/$', ticket_list, name='ticket-list'),
    url(r'^finance/ticket/create/$', TicketFormView.as_view(), name="get-ticketform"),
    url(r'^finance/ticket/edit/(?P<slug>[-\w\d]+)/$', ticket_record, name='ticket-detail'),
    url(r'^finance/ticket/delete/(?P<slug>[-\w\d]+)/$', ticket_delete, name='ticket-delete'),
    url(r'^finance/ticket/delete_confirm/(?P<slug>[-\w\d]+)/$', TicketDeleteConfirmView.as_view(),
        name='ticket-deleteconf'),
    url(r'^finance/merchandise/$', merchandise_list, name='merchandise-list'),
    url(r'^finance/merchandise/create/$', MerchandiseFormView.as_view(), name="get-merchandiseform"),
    url(r'^finance/merchandise/edit/(?P<slug>[-\w\d]+)/$', ticket_record, name='merchandise-detail'),
    url(r'^finance/merchandise/delete/(?P<slug>[-\w\d]+)/$', ticket_delete, name='merchandise-delete'),
    url(r'^finance/merchandise/delete_confirm/(?P<slug>[-\w\d]+)/$', MerchandiseDeleteConfirmView.as_view(),
        name='merchandise-deleteconf'),
    url(r'^finance/giftaid/$', giftaid_list, name='giftaid-list'),
    url(r'^finance/giftaid/create/$', GiftaidFormView.as_view(), name="get-giftaidform"),
    url(r'^finance/giftaid/edit/(?P<slug>[-\w\d]+)/$', giftaid_record, name='giftaid-detail'),
    url(r'^finance/giftaid/delete/(?P<slug>[-\w\d]+)/$', giftaid_delete, name='giftaid-delete'),
    url(r'^finance/giftaid/delete_confirm/(?P<slug>[-\w\d]+)/$', GiftaidDeleteConfirmView.as_view(),
        name='giftaid-deleteconf'),
    url(r'^finance/donation/$', donation_list, name='donation-list'),
    url(r'^finance/donation/create/$', DonationFormView.as_view(), name="get-donationform"),
    url(r'^finance/donation/edit/(?P<slug>[-\w\d]+)/$', donation_record, name='donation-detail'),
    url(r'^finance/donation/delete/(?P<slug>[-\w\d]+)/$', donation_delete, name='donation-delete'),
    url(r'^finance/donation/delete_confirm/(?P<slug>[-\w\d]+)/$', DonationDeleteConfirmView.as_view(),
        name='donation-deleteconf'),
    url(r'^finance/basket/$', basket_list, name='basket-list'),
    url(r'^finance/basket/create/$', BasketFormView.as_view(), name="get-basketform"),
    url(r'^finance/basket/edit/(?P<slug>[-\w\d]+)/$', basket_record, name='basket-detail'),
    url(r'^finance/basket/delete/(?P<slug>[-\w\d]+)/$', basket_delete, name='basket-delete'),
    url(r'^finance/basket/delete_confirm/(?P<slug>[-\w\d]+)/$', BasketDeleteConfirmView.as_view(),
        name='basket-deleteconf')
]
