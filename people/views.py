from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import RoleSerializer, PersonSerializer, Working_HrsSerializer, StaffSerializer, VolunteerSerializer
from .models import Role, Person, Working_Hrs, Staff, Volunteer


class RoleViewSet(ViewSet):

    def list(self, request):
        queryset = Role.objects.order_by('pk')
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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


class PersonViewSet(ViewSet):

    def list(self, request):
        queryset = Person.objects.order_by('pk')
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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


class Working_HrsViewSet(ViewSet):

    def list(self, request):
        queryset = Working_Hrs.objects.order_by('pk')
        serializer = Working_HrsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = Working_HrsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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


class StaffViewSet(ViewSet):

    def list(self, request):
        queryset = Staff.objects.order_by('pk')
        serializer = StaffSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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


class VolunteerViewSet(ViewSet):

    def list(self, request):
        queryset = Volunteer.objects.order_by('pk')
        serializer = VolunteerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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
