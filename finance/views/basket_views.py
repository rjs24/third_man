from django import shortcuts
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from ..forms import BasketForm
from ..serializers import BasketSerializer
from ..models import Basket
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


class APIBasketViewSet(ViewSet):

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
        item = shortcuts.get_object_or_404(queryset, slug=pk)
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


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class BasketViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'people/roles.html'

    def list(self, request):
        queryset = Basket.objects.order_by('pk')
        serializer = BasketSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/baskets.html')

    def create(self, request):
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Basket.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='finance/baskets.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Basket.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        serializer = BasketSerializer(item)
        form = BasketForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form':form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='finance/basket_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Basket.objects.get(slug=slug)
            except Basket.DoesNotExist:
                return Response(status=404)
            serializer = BasketSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Basket.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/baskets.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == 'POST':
            try:
                item = Basket.objects.get(slug=slug)
            except Basket.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(shortcuts.reverse('basket-list'))


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class BasketFormView(generic.FormView):
    form_class = BasketForm
    template_name = 'finance/basket_form_create.html'
    success_url = '/basket/'


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class BasketDeleteConfirmView(generic.DeleteView):
    queryset = Basket.objects.all()
    template_name = 'finance/basket_deleteconfirm.html'
    success_url = '/basket/'

    def get(self, request, slug):
        queryset = Basket.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'finance/basket_deleteconfirm.html', {'item': item, 'slug': slug})