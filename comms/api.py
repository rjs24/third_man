from rest_framework.routers import DefaultRouter
from .views import APICommsGroupViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'comms', APICommsGroupViewSet, basename='CommsGroup-list')
router.register(r'comms/(?P<slug>[-\w\d]+)/$', APICommsGroupViewSet, basename='CommsGroup-detail')
