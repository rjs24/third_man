"""third_man URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('', include('events.urls')),
    path('', include('comms.urls')),
    path('', include('finance.urls')),
    path('', include('people.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('django.contrib.auth.urls')),
    path('', include('configuration.urls')),
    path('landing/', TemplateView.as_view(template_name='registration/non_user.html'), name="nonuser"),
    path('accounts/sign_up/', views.sign_up, name="sign-up"),
    path('accounts/profile/', TemplateView.as_view(template_name="registration/user_profile.html"), name="sign-up"),
    path('logoutuser/', TemplateView.as_view(template_name='registration/logout.html'), name="logout"),
    path('logout/', TemplateView.as_view(template_name='registration/logged_out.html'), name="nonuser"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
