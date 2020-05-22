from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PersonViewSet, Working_HrsViewSet, StaffViewSet, VolunteerViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'roles', RoleViewSet, basename='Roles-list')
router.register(r'roles_detail', RoleViewSet, basename='Roles-detail')
router.register(r'person', PersonViewSet, basename='Person-list')
router.register(r'person_detail', PersonViewSet, basename='Person-detail')
router.register(r'working_hrs', Working_HrsViewSet, basename='WorkingHrs-list')
router.register(r'working_hrs_detail', Working_HrsViewSet, basename='WorkingHrs-detail')
router.register(r'staff', StaffViewSet, basename='Staff-list')
router.register(r'staff_detail', StaffViewSet, basename='Staff-detail')
router.register(r'volunteer', VolunteerViewSet, basename='Volunteer-list')
router.register(r'volunteer_detail', VolunteerViewSet, basename='Volunteer-detail')