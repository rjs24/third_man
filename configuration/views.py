from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission, GroupManager
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# class UserConfigView(ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'configuration/user_access_manager.html'
#
#     @method_decorator(login_required)
#     def list(self, request):
#         queryset = User.objects.all().order_by('pk')
#         serializer = CommsGroupSerializer(queryset, many=True)
#         return Response({'queryset': queryset}, template_name='comms/comms_group.html')
#
#     @method_decorator(login_required)
#     def create(self, request):
#         print(request.data)
#         serializer = CommsGroupSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             queryset = CommsGroup.objects.all().order_by('pk')
#             return Response({'queryset': queryset, 'serializer': serializer}, template_name='comms/comms_group.html',
#                             status=201)
#         return Response(serializer.errors, status=400)
#
#     @method_decorator(login_required)
#     def retrieve(self, request, slug):
#         queryset = CommsGroup.objects.all()
#         item = get_object_or_404(queryset, slug=slug)
#         serializer = CommsGroupSerializer(item)
#         form = CommsForm(instance=item)
#         slug = request.resolver_match.kwargs['slug']
#         return Response({'form': form, 'serializer': serializer, 'slug': slug, 'queryset': queryset},
#                         template_name='comms/comms_group_form_detail.html')
#
#     @method_decorator(login_required)
#     def update(self, request, slug):
#         if request.method == 'POST':
#             try:
#                 item = CommsGroup.objects.get(slug=slug)
#             except CommsGroup.DoesNotExist:
#                 return Response(status=404)
#             serializer = CommsGroupSerializer(item, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 queryset = CommsGroup.objects.all().order_by('pk')
#                 return Response({'queryset': queryset, 'serializer': serializer},
#                                 template_name='comms/comms_group.html', status=200)
#             return Response(serializer.errors, status=400)
#
#     @method_decorator(login_required)
#     def destroy(self, request, slug):
#         if request.method == "POST":
#             try:
#                 item = CommsGroup.objects.get(slug=slug)
#             except CommsGroup.DoesNotExist:
#                 return Response(status=404)
#             item.delete()
#             return shortcuts.redirect(reverse('comms-list'), status=204)