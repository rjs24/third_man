from django import shortcuts
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from ..forms import MerchandiseForm
from ..serializers import MerchandiseSerializer
from ..models import Merchandise
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


class APIMerchandiseViewSet(ViewSet):

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
        item = shortcuts.get_object_or_404(queryset, slug=pk)
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


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class MerchandiseViewSet(ModelViewSet):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'finance/merchandise.html'

    def list(self, request):
        queryset = Merchandise.objects.order_by('pk')
        serializer = MerchandiseSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/merchandise.html')

    def create(self, request):
        serializer = MerchandiseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Merchandise.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='finance/merchandise.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Merchandise.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        serializer = MerchandiseSerializer(item)
        form = MerchandiseForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form':form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='finance/merchandise_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Merchandise.objects.get(slug=slug)
            except Merchandise.DoesNotExist:
                return Response(status=404)
            serializer = MerchandiseSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Merchandise.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/merchandise.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == 'POST':
            try:
                item = Donation.objects.get(slug=slug)
            except Donation.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(shortcuts.reverse('merchandise-list'))


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class MerchandiseFormView(generic.FormView):
    form_class = MerchandiseForm
    template_name = 'finance/merchandise_form_create.html'
    success_url = '/merchandise/'


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class MerchandiseDeleteConfirmView(generic.DeleteView):
    queryset = Merchandise.objects.all()
    template_name = 'finance/merchandise_deleteconfirm.html'
    success_url = '/merchandise/'

    def get(self, request, slug):
        queryset = Merchandise.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'finance/merchandise_deleteconfirm.html', {'item': item, 'slug': slug})
