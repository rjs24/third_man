from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from rest_framework.response import Response
from ..serializers import StaffSerializer
from ..models import Staff
from django import shortcuts
from ..forms import StaffForm


class APIStaffViewSet(ModelViewSet):

    def list(self, request):
        queryset = Staff.objects.order_by('pk')
        serializer = StaffSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Staff status': 'staff created'}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Staff.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = StaffSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Staff.objects.get(slug=pk)
        except Staff.DoesNotExist:
            return Response(status=404)
        serializer = StaffSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Staff.objects.get(slug=pk)
        except Staff.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "people/staff.html"

    @method_decorator(login_required)
    def list(self, request):
        queryset = Staff.objects.order_by('pk')
        serializer = StaffSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/staff.html')

    @method_decorator(login_required)
    def create(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Staff.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/staff.html',
                            status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def retrieve(self, request, slug):
        queryset = Staff.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        serializer = StaffSerializer(item)
        form = StaffForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form': form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='people/staff_detail.html')

    @method_decorator(login_required)
    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Staff.objects.get(slug=slug)
            except Staff.DoesNotExist:
                return Response(status=404)
            serializer = StaffSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Staff.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/staff.html', status=200)
            return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def destroy(self, request, slug):
        if request.method == "POST":
            try:
                item = Staff.objects.get(slug=slug)
            except Staff.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(reverse('staff-list'), status=204)


class StaffFormView(generic.FormView):
    form_class = StaffForm
    template_name = 'people/staff_form_create.html'
    success_url = "/people/staff/"


class StaffDeleteConfirmView(generic.DeleteView):
    queryset = Staff.objects.all()
    template_name = 'people/staff_deleteconfirm.html'
    success_url = '/people/staff/'

    def get(self, request, slug):
        queryset = Staff.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'people/staff_deleteconfirm.html', {'item': item, 'slug': slug})