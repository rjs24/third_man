from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'

    def home_page_render(self, request):
        return render(request, {'user': request.user.username })
