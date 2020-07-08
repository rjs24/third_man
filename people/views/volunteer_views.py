from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from rest_framework.response import Response
from ..serializers import VolunteerSerializer
from ..models import Volunteer
from django import shortcuts
from ..forms import VolunteerForm


class APIVolunteerViewSet(ModelViewSet):

    def list(self, request):
        queryset = Volunteer.objects.order_by('pk')
        serializer = VolunteerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Volunteer status': 'Volunteer created'}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Volunteer.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = VolunteerSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Volunteer.objects.get(slug=pk)
        except Volunteer.DoesNotExist:
            return Response(status=404)
        serializer = VolunteerSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Volunteer.objects.get(slug=pk)
        except Volunteer.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class VolunteerViewSet(ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "people/volunteer.html"

    def list(self, request):
        queryset = Volunteer.objects.order_by('pk')
        serializer = VolunteerSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/volunteer.html')

    def create(self, request):
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Volunteer.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/volunteer.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Volunteer.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        serializer = VolunteerSerializer(item)
        form = VolunteerForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form': form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='people/volunteer_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Volunteer.objects.get(slug=slug)
            except Volunteer.DoesNotExist:
                return Response(status=404)
            serializer = VolunteerSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Volunteer.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/volunteer.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == "POST":
            try:
                item = Volunteer.objects.get(slug=slug)
            except Volunteer.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(reverse('volunteer-list'), status=204)


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class VolunteerFormView(generic.FormView):
    form_class = VolunteerForm
    template_name = 'people/volunteer_form_create.html'
    success_url = "/people/volunteer/"


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class VolunteerDeleteConfirmView(generic.DeleteView):
    queryset = Volunteer.objects.all()
    template_name = 'people/volunteer_deleteconfirm.html'
    success_url = '/people/volunteer/'

    def get(self, request, slug):
        queryset = Volunteer.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'people/volunteer_deleteconfirm.html', {'item': item, 'slug': slug})