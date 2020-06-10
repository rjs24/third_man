from rest_framework.routers import DefaultRouter
from .views import APIEventViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'event', APIEventViewSet, basename='events-list')
router.register(r'event_detail/(?P<slug>[-\w\d]+)/$', APIEventViewSet, basename='events-detail')