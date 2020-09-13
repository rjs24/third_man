from django import shortcuts
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from ..serializers import TicketSerializer
from ..models import Ticket
from ..forms import TicketForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


class APITicketViewSet(ViewSet):

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
        item = shortcuts.get_object_or_404(queryset, slug=pk)
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


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'finance/tickets.html'

    def list(self, request):
        queryset = Ticket.objects.order_by('pk')
        serializer = TicketSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/tickets.html')

    def create(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Ticket.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='finance/tickets.html',
                            status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Ticket.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        serializer = TicketSerializer(item)
        form = TicketForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form':form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='finance/donation_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Ticket.objects.get(slug=slug)
            except Ticket.DoesNotExist:
                return Response(status=404)
            serializer = TicketSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Ticket.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='finance/tickets.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        if request.method == 'POST':
            try:
                item = Ticket.objects.get(slug=slug)
            except Ticket.DoesNotExist:
                return Response(status=404)
            item.delete()
            return shortcuts.redirect(shortcuts.reverse('ticket-list'))


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class TicketFormView(generic.FormView):
    form_class = TicketForm
    template_name = 'finance/ticket_form_create.html'
    success_url = '/ticket/'


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class TicketDeleteConfirmView(generic.DeleteView):
    queryset = Ticket.objects.all()
    template_name = 'finance/ticket_deleteconfirm.html'
    success_url = '/ticket/'

    def get(self, request, slug):
        queryset = Ticket.objects.all()
        item = shortcuts.get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'finance/ticket_deleteconfirm.html', {'item': item, 'slug': slug})