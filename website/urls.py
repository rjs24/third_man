from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^admin/home/$', index, name='home'),
    ]