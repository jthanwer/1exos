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

from .models import Exercice, Correction, Rating
from .serializers import ExerciceSerializer, CorrectionSerializer, \
    PreviewCorrectionSerializer, RatingSerializer
from .filters import ExerciceFilter

import core.fluxes as fluxes

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
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
        file = serializer.validated_data.get('file', None)
        exercice = serializer.save(posteur=user, niveau=user.niveau,
                                   prefix_prof=user.prefix_prof,
                                   nom_prof=user.nom_prof,
                                   ville_etablissement=user.ville_etablissement,
                                   nom_etablissement=user.nom_etablissement,
                                   file=None)

        if file:
            old_filename = file.name
            extension = old_filename.split('.')[-1].lower()
            fileid = exercice.id
            if extension != 'pdf':
                image = Image.open(file)
                output = BytesIO()
                format_file = 'JPEG' if extension.lower() == 'jpg' else extension.upper()
                image.save(output, format=format_file, quality=20)
                output.seek(0)

                filename = 'Exercice{}.'.format(fileid) + extension
                file = InMemoryUploadedFile(output, 'ImageField', filename,
                                            'image/{}'.format(format_file.lower()),
                                            sys.getsizeof(output), None)
            else:
                file.name = 'Exercice{}.'.format(fileid) + extension

            exercice.file = file
            exercice.save()

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
        file = serializer.validated_data.get('file', None)
        enonceid = serializer.validated_data.get('enonce_id', None)
        correction = serializer.save(correcteur=correcteur, file=None)

        if file:
            old_filename = file.name
            extension = old_filename.split('.')[-1].lower()
            fileid = correction.id
            if extension != 'pdf':
                image = Image.open(file)
                output = BytesIO()
                format_file = 'JPEG' if extension.lower() == 'jpg' else extension.upper()
                image.save(output, format=format_file, quality=20)
                output.seek(0)

                filename = 'Correction{}-{}.'.format(enonceid, fileid) + extension
                file = InMemoryUploadedFile(output, 'ImageField', filename,
                                            'image/{}'.format(format_file.lower()),
                                            sys.getsizeof(output), None)
            else:
                file.name = 'Correction{}.'.format(fileid) + extension

            correction.file = file
            correction.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        correction = self.get_object()
        fluxes.delete_correction(correction)
        correction.file.delete(save=True)
        correction.delete()
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

    @action(methods=['get'], detail=True, permission_classes=[AllowAny],
            parser_classes=[JSONParser])
    def get_ratings(self, request, pk=None):
        correction = self.get_object()
        ratings = correction.ratings.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


# -------------
# -- Rating
# -------------
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        voter = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(voter=voter)

# import boto3
# from botocore.client import Config
# s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
# url = s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': '1exo-assets','Key': 'media/private/Correction4-12.jpg'}, ExpiresIn=5)
# print(url)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
