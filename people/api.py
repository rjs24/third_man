from rest_framework.routers import DefaultRouter
from .views.role_views import APIRoleViewSet
from .views.person_views import APIPersonViewSet
from .views.wk_hrs_views import APIWorking_HrsViewSet
from .views.staff_views import APIStaffViewSet
from .views.volunteer_views import APIVolunteerViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'people/roles', APIRoleViewSet, basename='roles-list')
router.register(r'people/roles/(?P<slug>[-\w\d]+)/$', APIRoleViewSet, basename='roles-detail')
router.register(r'people/person', APIPersonViewSet, basename='person-list')
router.register(r'people/person/(?P<slug>[-\w\d]+)/$', APIPersonViewSet, basename='person-detail')
router.register(r'people/wk_hrs', APIWorking_HrsViewSet, basename='hrs-list')
router.register(r'people/wk_hrs/(?P<slug>[-\w\d]+)/$', APIWorking_HrsViewSet, basename='hrs-detail')
router.register(r'people/staff', APIStaffViewSet, basename='staff-list')
router.register(r'people/staff/(?P<slug>[-\w\d]+)/$', APIStaffViewSet, basename='staff-detail')
router.register(r'people/volunteer', APIVolunteerViewSet, basename='volunteer-list')
router.register(r'people/volunteer/(?P<slug>[-\w\d]+)/$', APIVolunteerViewSet, basename='volunteer-detail')

