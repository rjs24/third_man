from rest_framework.routers import DefaultRouter
from .views import APIEventViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'events', APIEventViewSet, basename='Events-list')
router.register(r'events/(?P<slug>[-\w\d]+)/$', APIEventViewSet, basename='Events-detail')