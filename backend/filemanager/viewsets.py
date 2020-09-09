from rest_framework import generics, status, viewsets, renderers, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.http import Http404, FileResponse
from django.core import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile

from django_filters.rest_framework import DjangoFilterBackend

from .models import Exercice, Correction, Rating
from .serializers import ExerciceSerializer, CorrectionSerializer, \
    PreviewCorrectionSerializer, RatingSerializer
from .filters import ExerciceFilter
from .permissions import IsBuyer

import core.fluxes as fluxes
import core.files as files
import core.constants as cst

import os
import sys
from PIL import Image
from io import BytesIO


CONTENT_TYPES = {''}


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
        exercice = serializer.save(posteur=user,
                                   option=user.option,
                                   prefix_prof=user.prefix_prof,
                                   nom_prof=user.nom_prof,
                                   ville_etablissement=user.ville_etablissement,
                                   nom_etablissement=user.nom_etablissement,
                                   file=None)

        if file:
            # try:
            exercice.file = files.compress_file(file, exercice.id)
            exercice.save()
            # except:
            #     exercice.delete()
            #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        queryset = Correction.objects.filter(enonce=exercice).order_by('date_created')

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

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def my_liked_exercices(self, request):
        posteur = request.user
        queryset = Exercice.objects.filter(liked_by=posteur)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# -------------
# -- Correction
# -------------
class CorrectionViewSet(viewsets.ModelViewSet):
    queryset = Correction.objects.all().order_by('-date_created')
    serializer_class = CorrectionSerializer

    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ['retrieve']:
            permission_classes = [IsBuyer]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        correcteur = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data.get('file', None)
        enonceid = serializer.validated_data.get('enonce_id', None)
        correction = serializer.save(correcteur=correcteur,
                                     prix=cst.START_CORREC_PRICE(), file=None)

        if file:
            try:
                correction.file = files.compress_file(file, correction.id, enonce_id=enonceid)
                fluxes.submit_correction(correction)
                correction.save()
            except:
                correction.delete()
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        # -- L'utilisateur ne paye pas s'il possède déjà la correction
        if user.unlocked_correcs.filter(id=correction.id).exists():
            return Response(status=status.HTTP_200_OK)

        # -- Fait le transfert d'argent si possible
        if not fluxes.buy_correction(user, correction):
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

        # -- Débloque toutes les corrections de l'exo
        all_corrections = correction.enonce.correcs.all()
        for elt in all_corrections:
            user.unlocked_correcs.add(elt)

        data = CorrectionSerializer(correction).data

        return Response(data, status=status.HTTP_200_OK)

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
        rating = serializer.save(voter=voter)

        # -- Si le posteur de l'exo met une note inférieure à 4,
        # on supprime la correction et on fait des transferts de points
        if voter == rating.correc.enonce.posteur and rating.value < 4:
            correction = rating.correc
            fluxes.delete_correction(correction)
            correction.file.delete(save=True)
            correction.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        voter = request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        rating = serializer.save()

        # -- Si le posteur de l'exo met une note inférieure à 4,
        # on supprime la correction et on fait des transferts de points
        if voter == rating.correc.enonce.posteur and rating.value < 4:
            correction = rating.correc
            fluxes.delete_correction(correction)
            correction.file.delete(save=True)
            correction.delete()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
