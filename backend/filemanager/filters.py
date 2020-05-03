from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Exercice


class ExerciceFilter(filters.FilterSet):
    posteur__prof = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Exercice
        fields = ['posteur__classe', 'posteur__prof', 'posteur__etablissement',
                  'category', 'livre', 'num_page', 'num_exo']

