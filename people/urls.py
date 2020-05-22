from rest_framework.routers import DefaultRouter
from . import views
from django.urls import include, path


router = DefaultRouter()

router.register(r'api/role', views.RoleViewSet, 'Role')
router.register(r'api/person', views.PersonViewSet, 'Person')
router.register(r'api/working_hrs', views.Working_HrsViewSet, 'Working_Hrs')
router.register(r'api/staff', views.StaffViewSet, 'Staff')
router.register(r'api/volunteer', views.VolunteerViewSet, 'Volunteer')

urlpatterns = router.urls

app_name = 'people'
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]