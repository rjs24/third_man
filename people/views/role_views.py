from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from ..serializers import RoleSerializer
from ..models import Role
from django import shortcuts
from ..forms import RoleForm


class APIRoleViewSet(ModelViewSet):

    def list(self, request):
        queryset = Role.objects.order_by('pk')
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Role status': 'New role created'}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Role.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = RoleSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Role.objects.get(slug=pk)
        except Role.DoesNotExist:
            return Response(status=404)
        serializer = RoleSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Role.objects.get(slug=pk)
        except Role.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'people/roles.html'

    def list(self, request):
        queryset = Role.objects.order_by('pk')
        serializer = RoleSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/roles.html')

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Role.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='people/roles.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Role.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        serializer = RoleSerializer(item)
        form = RoleForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form':form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='people/role_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Role.objects.get(slug=slug)
            except Role.DoesNotExist:
                return Response(status=404)
            serializer = RoleSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Role.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/roles.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == 'POST':
            try:
                item = Role.objects.get(slug=slug)
            except Role.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(reverse('roles-list'))


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class RoleFormView(generic.FormView):
    form_class = RoleForm
    template_name = 'people/role_form_create.html'
    success_url = "/people/roles/"


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class RoleDeleteConfirmView(generic.DeleteView):
    queryset = Role.objects.all()
    template_name = 'people/role_deleteconfirm.html'
    success_url = '/people/roles/'

    def get(self, request, slug):
        queryset = Role.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'people/role_deleteconfirm.html', {'item': item, 'slug': slug})