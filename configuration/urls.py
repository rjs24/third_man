from django.conf.urls import include, url
from .views import *

user_list = UserViewSet.as_view({
    'get':'list',
    'post':'create',
})

user_record = UserViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

user_delete = UserViewSet.as_view({
    'post':'destroy'
})

group_list = GroupViewSet.as_view({
    'get':'list',
    'post':'create',
})

group_record = GroupViewSet.as_view({
    'get':'retrieve',
    'post':'update'
})

group_delete = GroupViewSet.as_view({
    'post':'destroy'
})

# app_list = AppViewSet.as_view({
#     'get': 'list'
# })
#
# app_detail = AppViewSet.as_view({
#     'get': 'retrieve',
#     'post': 'update'
# })


urlpatterns = [
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/edit/(?P<pk>[0-9])/$', user_record, name='user-detail'),
    url(r'^users/create/$', UserFormView.as_view(), name="get-userform"),
    url(r'^users/delete_confirm/(?P<pk>[0-9])/$', UserDeleteConfirmView.as_view(), name='users-deleteconf'),
    url(r'^users/delete/(?P<pk>[0-9])/$', user_delete, name='user-delete'),
    url(r'^groups/$', group_list, name='group-list'),
    url(r'^groups/edit/(?P<pk>[0-9])/$', group_record, name='group-detail'),
    url(r'^groups/create/$', GroupFormView.as_view(), name="get-groupform"),
    url(r'^groups/delete_confirm/(?P<pk>[0-9])/$', GroupDeleteConfirmView.as_view(), name='groups-deleteconfirm'),
    url(r'^groups/delete/(?P<pk>[0-9])/$', group_delete, name='group-delete'),
    # url('apps/', app_list, name='app-list'),
    # url(r'apps/edit/(<slug>[-\w\d]+)/', app_record, name='app-detail'),
    url(r'^settings/$', ConfigViewHome.as_view(), name='config'),
]