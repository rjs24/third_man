from django import shortcuts
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from ..serializers import GiftaidSerializer
from ..models import Giftaid
from ..forms import GiftaidForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


class APIGiftaidViewSet(ViewSet):
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


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class GiftaidViewSet(ModelViewSet):
    queryset = Giftaid.objects.all()
    serializer_class = GiftaidSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'finance/giftaid.html'

    def list(self, request):
        queryset = Giftaid.objects.order_by('pk')
        serializer = GiftaidSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/giftaid.html')

    def create(self, request):
        serializer = GiftaidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Giftaid.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='finance/giftaid.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Giftaid.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        serializer = GiftaidSerializer(item)
        form = GiftaidForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form':form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='finance/giftaid_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Giftaid.objects.get(slug=slug)
            except Giftaid.DoesNotExist:
                return Response(status=404)
            serializer = GiftaidSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Giftaid.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/giftaid.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == 'POST':
            try:
                item = Giftaid.objects.get(slug=slug)
            except Giftaid.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(shortcuts.reverse('giftaid-list'))


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class GiftaidFormView(generic.FormView):
    form_class = GiftaidForm
    template_name = 'finance/giftaid_form_create.html'
    success_url = '/giftaid/'


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class GiftaidDeleteConfirmView(generic.DeleteView):
    queryset = Giftaid.objects.all()
    template_name = 'finance/giftaid_deleteconfirm.html'
    success_url = '/giftaid/'

    def get(self, request, slug):
        queryset = Giftaid.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'finance/giftaid_deleteconfirm.html', {'item': item, 'slug': slug})