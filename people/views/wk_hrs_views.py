from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from rest_framework.response import Response
from ..serializers import Working_HrsSerializer
from ..models import Working_Hrs
from django import shortcuts
from ..forms import WorkingHoursForm


class APIWorking_HrsViewSet(ModelViewSet):

    def list(self, request):
        queryset = Working_Hrs.objects.order_by('pk')
        serializer = Working_HrsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = Working_HrsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Working_Hrs status': 'Working_Hrs created'}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Working_Hrs.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = Working_HrsSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Working_Hrs.objects.get(slug=pk)
        except Working_Hrs.DoesNotExist:
            return Response(status=404)
        serializer = Working_HrsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Working_Hrs.objects.get(slug=pk)
        except Working_Hrs.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class Working_HrsViewSet(ModelViewSet):
    queryset = Working_Hrs.objects.all()
    serializer_class = Working_HrsSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "people/working_hrs.html"

    def list(self, request):
        queryset = Working_Hrs.objects.order_by('pk')
        serializer = Working_HrsSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/working_hrs.html')

    def create(self, request):
        serializer = Working_HrsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Working_Hrs.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/working_hrs.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Working_Hrs.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        serializer = Working_HrsSerializer(item)
        form = WorkingHoursForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form': form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='people/working_hrs_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Working_Hrs.objects.get(slug=slug)
            except Working_Hrs.DoesNotExist:
                return Response(status=404)
            serializer = Working_HrsSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Working_Hrs.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/working_hrs.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == "POST":
            try:
                item = Working_Hrs.objects.get(slug=slug)
            except Working_Hrs.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(reverse('working_hrs-list'), status=204)


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class Working_HrsFormView(generic.FormView):
    form_class = WorkingHoursForm
    template_name = 'people/working_hrs_form_create.html'
    success_url = "/people/working_hrs/"


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class Working_HrsDeleteConfirmView(generic.DeleteView):
    queryset = Working_Hrs.objects.all()
    template_name = 'people/working_hrs_deleteconfirm.html'
    success_url = '/people/working_hrs/'

    def get(self, request, slug):
        queryset = Working_Hrs.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'people/working_hrs_deleteconfirm.html', {'item': item, 'slug': slug})