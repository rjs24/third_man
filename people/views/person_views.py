from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from rest_framework.response import Response
from ..serializers import RoleSerializer, PersonSerializer, Working_HrsSerializer, StaffSerializer, VolunteerSerializer
from ..models import Role, Person, Working_Hrs, Staff, Volunteer
from django import shortcuts
from ..forms import PersonForm


class APIPersonViewSet(ModelViewSet):

    def list(self, request):
        queryset = Person.objects.order_by('pk')
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Person status': 'person created'}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Person.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = PersonSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Person.objects.get(slug=pk)
        except Person.DoesNotExist:
            return Response(status=404)
        serializer = PersonSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Person.objects.get(slug=pk)
        except Person.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'people/persons.html'

    @method_decorator(login_required)
    def list(self, request):
        queryset = Person.objects.order_by('pk')
        serializer = PersonSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer':serializer}, template_name='people/persons.html')

    @method_decorator(login_required)
    def create(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Person.objects.all()
            return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/persons.html',
                            status=201)
        return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def retrieve(self, request, slug):
        queryset = Person.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        serializer = PersonSerializer(item)
        form = PersonForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form': form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='people/person_detail.html')

    @method_decorator(login_required)
    def update(self, request, slug):
        if request.method == "POST":
            try:
                item = Person.objects.get(slug=slug)
            except Person.DoesNotExist:
                return Response(status=404)
            serializer = PersonSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Person.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='people/persons.html',
                                status=200)
            return Response(serializer.errors, status=400)

    @method_decorator(login_required)
    def destroy(self, request, slug):
        try:
            item = Person.objects.get(slug=slug)
        except Person.DoesNotExist:
            return Response(status=404)
        item.delete()
        return shortcuts.redirect(reverse('person-list'))


class PersonFormView(generic.FormView):
    form_class = PersonForm
    template_name = 'people/person_form_create.html'
    success_url = "/people/person/"


class PersonDeleteConfirmView(generic.DeleteView):
    queryset = Role.objects.all()
    template_name = 'people/person_deleteconfirm.html'
    success_url = '/people/person/'

    def get(self, request, slug):
        queryset = Person.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'people/person_deleteconfirm.html', {'item': item, 'slug': slug})