from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CalendarView, EventsFormView, EventDeleteConfirmView
from django.conf.urls import include, url
from .api import router

event_list = EventViewSet.as_view({
    'get':'list',
    'post':'create',
})

event_record = EventViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

event_delete = EventViewSet.as_view({
    'post':'destroy'
})


urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'^event/$', event_list, name='event-list'),
    url(r'^event/create/$', EventsFormView.as_view(), name="get-form"),
    url(r'^event/edit/(?P<slug>[-\w\d]+)/$', event_record, name='event-detail'),
    url(r'^event/delete/(?P<slug>[-\w\d]+)/$', event_delete, name='event-delete'),
    url(r'^event/delete_confirm/(?P<slug>[-\w\d]+)/$', EventDeleteConfirmView.as_view(), name='event-deleteconf'),
    url(r'calendar/', CalendarView.as_view(), name='events_calendar.html'),
]
