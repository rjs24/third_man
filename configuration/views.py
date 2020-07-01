from django.contrib.auth.models import User, Group
from django.contrib.auth import login

from django.shortcuts import get_object_or_404

from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from .serializers import UserSerializer, GroupSerializer
from django import shortcuts
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.views import View
from .forms import GroupForm


class ConfigViewHome(View):
    template_name = 'configuration/configuration_home.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'configuration/configuration_home.html')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'configuration/users.html'

    @method_decorator(login_required, permission_required)
    def list(self, request):
        queryset = User.objects.all().order_by('pk')
        serializer = UserSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='configuration/users.html')

    @method_decorator(login_required, permission_required)
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = User.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer}, template_name='configuration/users.html', status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(login_required, permission_required)
    def retrieve(self, request, pk):
        queryset = User.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(item)
        form = UserChangeForm(instance=item)
        pk = request.resolver_match.kwargs['pk']
        return Response({'form': form, 'serializer': serializer, 'pk':pk, 'queryset':queryset}, template_name='configuration/user_form_detail.html')

    @method_decorator(login_required, permission_required)
    def update(self, request, pk):
        if request.method == 'POST':
            try:
                item = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(status=404)
            serializer = UserSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = User.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='configuration/user_form_detail.html', status=200)
            return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def destroy(self, request, pk):
        if request.method == "POST":
            try:
                item = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(reverse('user-list'), status=204)


class UserFormView(generic.FormView):
    form_class = UserCreationForm
    template_name = 'configuration/user_form_create.html'
    success_url = '/users/'


class UserDeleteConfirmView(generic.DeleteView):
    queryset = User.objects.all()
    template_name = 'configuration/user_deleteconfirm.html'
    success_url = '/users/'

    def get(self, request, pk):
        queryset = User.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        return shortcuts.render(request, 'configuration/user_deleteconfirm.html', {'item': item, 'pk': pk})


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'configuration/groups.html'

    @method_decorator(login_required, permission_required)
    def list(self, request):
        queryset = Group.objects.all().order_by('pk')
        serializer = GroupSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='configuration/groups.html')

    @method_decorator(login_required, permission_required)
    def create(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Group.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer}, template_name='configuration/groups.html', status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(login_required, permission_required)
    def retrieve(self, request, pk):
        queryset = User.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(item)
        form = GroupForm(instance=item)
        return Response({'form': form, 'serializer': serializer, 'pk':pk, 'queryset':queryset}, template_name='configuration/group_form_detail.html')

    @method_decorator(login_required, permission_required)
    def update(self, request, pk):
        if request.method == 'POST':
            try:
                item = Group.objects.get(pk=pk)
            except Group.DoesNotExist:
                return Response(status=404)
            serializer = GroupSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Group.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='configuration/group_form_detail.html', status=200)
            return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def destroy(self, request, pk):
        if request.method == "POST":
            try:
                item = Group.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(reverse('user-list'), status=204)


class GroupFormView(generic.FormView):
    form_class = GroupForm
    template_name = 'configuration/group_form_create.html'
    success_url = '/groups/'


class GroupDeleteConfirmView(generic.DeleteView):
    queryset = User.objects.all()
    template_name = 'configuration/group_deleteconfirm.html'
    success_url = '/groups/'

    def get(self, request, pk):
        queryset = Group.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        return shortcuts.render(request, 'configuration/group_deleteconfirm.html', {'item': item, 'pk': pk})