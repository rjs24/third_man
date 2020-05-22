from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from .serializers import CommsGroupSerializer
from .models import CommsGroup
from django import shortcuts
from .forms import CommsForm


class APICommsGroupViewSet(ModelViewSet):
    def list(self, request):
        queryset = CommsGroup.objects.all().order_by('pk')
        serializer = CommsGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CommsGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"comms status": "comms group created"}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = CommsGroup.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = CommsGroupSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = CommsGroup.objects.get(slug=pk)
        except CommsGroup.DoesNotExist:
            return Response(status=404)
        serializer = CommsGroupSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = CommsGroup.objects.get(slug=pk)
        except CommsGroup.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class CommsGroupViewSet(ModelViewSet):
    queryset = CommsGroup.objects.all()
    serializer_class = CommsGroupSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'comms/comms_group.html'

    @method_decorator(login_required)
    def list(self, request):
        queryset = CommsGroup.objects.all().order_by('pk')
        serializer = CommsGroupSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='comms/comms_group.html')

    @method_decorator(login_required)
    def create(self, request):
        serializer = CommsGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = CommsGroup.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer}, template_name='comms/comms_group.html', status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def retrieve(self, request, slug):
        queryset = CommsGroup.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        serializer = CommsGroupSerializer(item)
        form = CommsForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form': form, 'serializer': serializer, 'slug':slug, 'queryset':queryset}, template_name='comms/comms_group_form_detail.html')

    @method_decorator(login_required)
    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = CommsGroup.objects.get(slug=slug)
            except CommsGroup.DoesNotExist:
                return Response(status=404)
            serializer = CommsGroupSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = CommsGroup.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='comms/comms_group.html', status=200)
            return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def destroy(self, request, slug):
        if request.method == "POST":
            try:
                item = CommsGroup.objects.get(slug=slug)
            except CommsGroup.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(reverse('comms-list'), status=204)


class CommsFormView(generic.FormView):
    form_class = CommsForm
    template_name = 'comms/comms_group_form_create.html'
    success_url = "/comms/"


class CommsDeleteConfirmView(generic.DeleteView):
    queryset = CommsGroup.objects.all()
    template_name = 'comms/comms_group_deleteconfirm.html'
    success_url = '/comms/'

    def get(self, request, slug):
        queryset = CommsGroup.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'comms/comms_group_deleteconfirm.html', {'item': item, 'slug':slug})

