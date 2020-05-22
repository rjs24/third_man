from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import TicketSerializer, MerchandiseSerializer, GiftaidSerializer, DonationSerializer, BasketSerializer
from .models import Ticket, Merchandise, Giftaid, Donation, Basket


class TicketViewSet(ViewSet):

    def list(self, request):
        queryset = Ticket.objects.order_by('pk')
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Ticket.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = TicketSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Ticket.objects.get(slug=pk)
        except Ticket.DoesNotExist:
            return Response(status=404)
        serializer = TicketSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Ticket.objects.get(slug=pk)
        except Ticket.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MerchandiseViewSet(ViewSet):

    def list(self, request):
        queryset = Merchandise.objects.order_by('pk')
        serializer = MerchandiseSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MerchandiseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Merchandise.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = MerchandiseSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Merchandise.objects.get(slug=pk)
        except Merchandise.DoesNotExist:
            return Response(status=404)
        serializer = MerchandiseSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Merchandise.objects.get(slug=pk)
        except Merchandise.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class GiftaidViewSet(ViewSet):

    def list(self, request):
        queryset = Giftaid.objects.order_by('pk')
        serializer = GiftaidSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = GiftaidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Giftaid.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = GiftaidSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Giftaid.objects.get(slug=pk)
        except Giftaid.DoesNotExist:
            return Response(status=404)
        serializer = GiftaidSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Giftaid.objects.get(slug=pk)
        except Giftaid.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class DonationViewSet(ViewSet):

    def list(self, request):
        queryset = Donation.objects.order_by('pk')
        serializer = DonationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Donation.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = DonationSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Donation.objects.get(slug=pk)
        except Donation.DoesNotExist:
            return Response(status=404)
        serializer = DonationSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Donation.objects.get(slug=pk)
        except Donation.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class BasketViewSet(ViewSet):

    def list(self, request):
        queryset = Basket.objects.order_by('pk')
        serializer = BasketSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Basket.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = BasketSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Basket.objects.get(slug=pk)
        except Basket.DoesNotExist:
            return Response(status=404)
        serializer = BasketSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Basket.objects.get(slug=pk)
        except Basket.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
