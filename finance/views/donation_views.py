from django import shortcuts
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from ..forms import DonationForm
from ..serializers import DonationSerializer
from ..models import Donation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


class APIDonationViewSet(ViewSet):

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
        item = shortcuts.get_object_or_404(queryset, slug=pk)
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


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class DonationViewSet(ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'finance/donations.html'

    def list(self, request):
        queryset = Donation.objects.order_by('pk')
        serializer = DonationSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/donations.html')

    def create(self, request):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Donation.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='finance/donations.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Donation.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        serializer = DonationSerializer(item)
        form = DonationForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form':form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='finance/donation_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Donation.objects.get(slug=slug)
            except Donation.DoesNotExist:
                return Response(status=404)
            serializer = DonationSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Donation.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/donations.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == 'POST':
            try:
                item = Donation.objects.get(slug=slug)
            except Donation.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(shortcuts.reverse('donation-list'))


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class DonationFormView(generic.FormView):
    form_class = DonationForm
    template_name = 'finance/donation_form_create.html'
    success_url = '/donation/'


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class DonationDeleteConfirmView(generic.DeleteView):
    queryset = Donation.objects.all()
    template_name = 'finance/donation_deleteconfirm.html'
    success_url = '/donation/'

    def get(self, request, slug):
        queryset = Donation.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'finance/donation_deleteconfirm.html', {'item': item, 'slug': slug})