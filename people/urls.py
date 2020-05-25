from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from .api import router
from .views.role_views import RoleViewSet, RoleFormView, RoleDeleteConfirmView
from .views.person_views import PersonViewSet, PersonFormView, PersonDeleteConfirmView
from .views.wk_hrs_views import Working_HrsViewSet, Working_HrsFormView, Working_HrsDeleteConfirmView
from .views.staff_views import StaffViewSet, StaffFormView, StaffDeleteConfirmView
from .views.volunteer_views import VolunteerViewSet, VolunteerFormView, VolunteerDeleteConfirmView

role_list = RoleViewSet.as_view({
    'get':'list',
    'post':'create',
})

role_record = RoleViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

role_delete = RoleViewSet.as_view({
    'post':'destroy'
})

person_list = PersonViewSet.as_view({
    'get':'list',
    'post':'create',
})

person_record = PersonViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

person_delete = PersonViewSet.as_view({
    'post':'destroy'
})

staff_list = StaffViewSet.as_view({
    'get':'list',
    'post':'create',
})

staff_record = StaffViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

staff_delete = StaffViewSet.as_view({
    'post':'destroy'
})

volunteer_list = VolunteerViewSet.as_view({
    'get':'list',
    'post':'create',
})

volunteer_record = VolunteerViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

volunteer_delete = VolunteerViewSet.as_view({
    'post':'destroy'
})

working_hrs_list = Working_HrsViewSet.as_view({
    'get':'list',
    'post':'create',
})

working_hrs_record = Working_HrsViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

working_hrs_delete = Working_HrsViewSet.as_view({
    'post':'destroy'
})

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^people/roles/$', role_list, name='roles-list'),
    url(r'^people/roles/edit/(?P<slug>[-\w\d]+)/$', role_record, name='roles-detail'),
    url(r'^people/roles/delete/(?P<slug>[-\w\d]+)/$', role_delete, name='roles-delete'),
    url(r'^people/roles/delete_confirm/(?P<slug>[-\w\d]+)/$', RoleDeleteConfirmView.as_view(), name='roles-deleteconf'),
    url(r'^people/roles/create/$', RoleFormView.as_view(), name="get-roleform"),
    url(r'^people/person/$', person_list, name='person-list'),
    url(r'^people/person/edit/(?P<slug>[-\w\d]+)/$', person_record, name='person-detail'),
    url(r'^people/person/delete/(?P<slug>[-\w\d]+)/$', person_delete, name='person-delete'),
    url(r'^people/person/delete_confirm/(?P<slug>[-\w\d]+)/$', PersonDeleteConfirmView.as_view(), name='person-deleteconf'),
    url(r'^people/person/create/$', PersonFormView.as_view(), name="get-personform"),
    url(r'^people/staff/$', staff_list, name='staff-list'),
    url(r'^people/staff/edit/(?P<slug>[-\w\d]+)/$', staff_record, name='staff-detail'),
    url(r'^people/staff/delete/(?P<slug>[-\w\d]+)/$', staff_delete, name='staff-delete'),
    url(r'^people/staff/delete_confirm/(?P<slug>[-\w\d]+)/$', StaffDeleteConfirmView.as_view(), name='staff-deleteconf'),
    url(r'^people/staff/create/$', StaffFormView.as_view(), name="get-stafform"),
    url(r'^people/volunteer/$', volunteer_list, name='volunteer-list'),
    url(r'^people/volunteer/edit/(?P<slug>[-\w\d]+)/$', volunteer_record, name='volunteer-detail'),
    url(r'^people/volunteer/delete/(?P<slug>[-\w\d]+)/$', volunteer_delete, name='volunteer-delete'),
    url(r'^people/volunteer/delete_confirm/(?P<slug>[-\w\d]+)/$', VolunteerDeleteConfirmView.as_view(),name='volunteer-deleteconf'),
    url(r'^people/volunteer/create/$', VolunteerFormView.as_view(), name="get-volunteerform"),
    url(r'^people/working_hrs/$', working_hrs_list, name='workinghrs-list'),
    url(r'^people/working_hrs/edit/(?P<slug>[-\w\d]+)/$', working_hrs_record, name='workinghrs-detail'),
    url(r'^people/working_hrs/delete/(?P<slug>[-\w\d]+)/$', working_hrs_delete, name='workinghrs-delete'),
    url(r'^people/working_hrs/delete_confirm/(?P<slug>[-\w\d]+)/$', Working_HrsDeleteConfirmView.as_view(),name='workinghrs-deleteconf'),
    url(r'^people/working_hrs/create/$', Working_HrsFormView.as_view(), name="get-workinghrsform"),
]
