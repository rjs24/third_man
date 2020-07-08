from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import login


class HomePageView(TemplateView):
    template_name = 'index.html'

    def home_page_render(self, request):
        return render(request, {'user': request.user.username})


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'index.html')
    context['form']=form
    return render(request,'registration/signup.html',context)
