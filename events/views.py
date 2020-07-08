from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from .serializers import EventSerializer
from .models import Event
from django import shortcuts
from .forms import EventForm
from django.utils.safestring import mark_safe
from .calendar_tool import Event_Calendar
from datetime import datetime


class APIEventViewSet(ModelViewSet):

    def list(self, request):
        queryset = Event.objects.all().order_by('pk')
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Event status": "Event created"}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        item = get_object_or_404(queryset, slug=pk)
        serializer = EventSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Event.objects.get(slug=pk)
        except Event.DoesNotExist:
            return Response(status=404)
        serializer = EventSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Event.objects.get(slug=pk)
        except Event.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'events/events.html'

    def list(self, request):
        queryset = Event.objects.all().order_by('pk')
        serializer = EventSerializer(queryset, many=True)
        return Response({'queryset': queryset, 'serializer': serializer.data}, template_name='events/events.html')

    def create(self, request):
        print(request.data)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Event.objects.all().order_by('pk')
            return Response({'queryset': queryset, 'serializer': serializer},
                            template_name='events/events.html', status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, slug):
        queryset = Event.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        serializer = EventSerializer(item)
        form = EventForm(instance=item)
        slug = request.resolver_match.kwargs['slug']
        return Response({'form': form, 'serializer': serializer, 'slug':slug, 'queryset':queryset},
                        template_name='events/event_form_detail.html')

    def update(self, request, slug):
        if request.method == 'POST':
            try:
                item = Event.objects.get(slug=slug)
            except Event.DoesNotExist:
                return Response(status=404)
            serializer = EventSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                queryset = Event.objects.all().order_by('pk')
                return Response({'queryset': queryset, 'serializer': serializer}, template_name='events/events.html', status=200)
            return Response(serializer.errors, status=400)

    def destroy(self, request, slug):
        try:
            item = Event.objects.get(slug=slug)
        except Event.DoesNotExist:
            return Response(status=404)
        item.delete()
        return shortcuts.redirect(reverse('event-list'), status=204)


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class EventsFormView(generic.FormView):
    form_class = EventForm
    template_name = 'events/event_form_create.html'
    success_url = '/events/'


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class EventDeleteConfirmView(generic.DeleteView):
    queryset = Event.objects.all()
    template_name = 'events/event_deleteconfirm.html'
    success_url = '/events/'

    def get(self, request, slug):
        queryset = Event.objects.all()
        item = get_object_or_404(queryset, slug=slug)
        slug = request.resolver_match.kwargs['slug']
        return shortcuts.render(request, 'events/event_deleteconfirm.html', {'item': item, 'slug': slug})


@method_decorator(login_required(login_url="/landing/"), name="dispatch")
class CalendarView(generic.ListView):
    model = Event
    template_name = 'events/events_calendar.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        todays_date = get_date_now(self.request.GET.get('day', None))
        calendar = Event_Calendar(todays_date.year, todays_date.month)
        html_cal_rend = calendar.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal_rend)
        return context


def get_date_now(requested_day):
    if requested_day:
        yr, month = (int(x) for x in requested_day.split('-'))
        return datetime(yr, month, day=1)
    return datetime.today()

