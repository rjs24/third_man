from django.conf.urls import include, url
from .api import router
from .views import CommsGroupViewSet, CommsFormView, CommsDeleteConfirmView


comms_list = CommsGroupViewSet.as_view({
    'get':'list',
    'post':'create',
})

comms_record = CommsGroupViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

comms_delete = CommsGroupViewSet.as_view({
    'post':'destroy'
})


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^comms/$', comms_list, name='comms-list'),
    url(r'^comms/edit/(?P<slug>[-\w\d]+)/$', comms_record, name='comms-detail'),
    url(r'^comms/delete/(?P<slug>[-\w\d]+)/$', comms_delete, name='comms-delete'),
    url(r'^comms/delete_confirm/(?P<slug>[-\w\d]+)/$', CommsDeleteConfirmView.as_view(), name='comms-deleteconf'),
    url(r'^comms/create/$', CommsFormView.as_view(), name="get-form"),
]