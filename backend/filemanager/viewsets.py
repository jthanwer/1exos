from rest_framework import generics, status, viewsets, renderers, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.http import Http404, FileResponse
from django.core import serializers

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ExerciceSerializer, CorrectionSerializer, \
    PreviewCorrectionSerializer
from .models import Exercice, Correction
from .filters import ExerciceFilter

import core.fluxes as fluxes

from PIL import Image
import os

class PassthroughRenderer(renderers.BaseRenderer):
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


# -----------
# -- Exercice
# -----------
class ExerciceViewSet(viewsets.ModelViewSet):
    queryset = Exercice.objects.all().order_by('-date_created')
    serializer_class = ExerciceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExerciceFilter

    permission_classes = (AllowAny,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(posteur=user, niveau=user.classe,
                              prefix_prof=user.prefix_prof,
                              nom_prof=user.nom_prof,
                              ville_etablissement=user.ville_etablissement,
                              nom_etablissement=user.nom_etablissement)
        if obj.file:
            file = obj.file
            old_path = file.path
            old_name = file.name
            extension = old_name.split('.')[-1]
            if extension != 'pdf':
                print('compressing')
                print(os.stat(old_path).st_size)
                image = Image.open(file)
                image.save(old_path, optimize=True, quality=20)
                print(os.stat(old_path).st_size)
            file.name = 'Exercice{}.'.format(obj.id) + extension
            os.rename(old_path, file.path)
            obj.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=True)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, request, pk=None):
        instance = self.get_object()

        file_handle = instance.file.open()

        response = FileResponse(file_handle, content_type='whatever')
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(instance.file.name)

        return response

    @action(methods=['get'], detail=True)
    def like(self, request, pk=None):
        exercice = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user.liked_exos.add(exercice)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def dislike(self, request, pk=None):
        exercice = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user.liked_exos.remove(exercice)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, permission_classes=[AllowAny])
    def corrections(self, request, pk=None):
        exercice = self.get_object()
        queryset = Correction.objects.filter(enonce=exercice)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CorrectionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CorrectionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def my_posted_exercices(self, request):
        posteur = request.user
        queryset = Exercice.objects.filter(posteur=posteur)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def my_liked_exercices(self, request):
        posteur = request.user
        queryset = Exercice.objects.filter(liked_by=posteur)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# -------------
# -- Correction
# -------------
class CorrectionViewSet(viewsets.ModelViewSet):
    queryset = Correction.objects.all()
    serializer_class = CorrectionSerializer
    search_fields = ['file']
    filter_backends = (filters.SearchFilter,)

    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        correcteur = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        correction = serializer.save(correcteur=correcteur)
        if correction.file:
            file = correction.file
            old_name = file.name
            old_path = file.path
            extension = old_name.split('.')[-1].lower()
            if extension != 'pdf':
                print('compressing')
                print(os.stat(old_path).st_size)
                image = Image.open(file)
                image.save(old_path, optimize=True, quality=20)
                print(os.stat(old_path).st_size)
            file.name = 'Correction{}.'.format(correction.id) + extension
            os.rename(old_path, file.path)
            correction.save()

        fluxes.submit_correction(correction)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=True)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, request, pk=None):
        instance = self.get_object()
        file_handle = instance.file.open()
        response = FileResponse(file_handle, content_type='whatever')
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(instance.file.name)

        return response

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def my_posted_corrections(self, request):
        user = request.user
        queryset = Correction.objects.filter(correcteur=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def my_unlocked_corrections(self, request):
        user = request.user
        queryset = Correction.objects.filter(buyers=user).exclude(correcteur=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[AllowAny],
            parser_classes=[JSONParser])
    def collect_unlock(self, request, pk=None):
        correction = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not fluxes.buy_correction(user, correction):
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        return Response(status=status.HTTP_200_OK)
