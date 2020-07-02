from rest_framework import generics
from django_filters import rest_framework as filters
from django.db.models import Count
from .models import Exercice


class ExerciceFilter(filters.FilterSet):
    posteur__nom_prof = filters.CharFilter(lookup_expr='icontains')
    is_corrected = filters.BooleanFilter(field_name='correcs', method='filter_is_corrected')
    is_from_livre = filters.BooleanFilter(field_name='livre', method='filter_is_from_livre')

    def filter_is_corrected(self, queryset, name, value):
        qs = queryset.annotate(num_c=Count(name))
        results = qs.filter(num_c__gte=1) if value else qs.filter(num_c__lte=0)
        return results

    def filter_is_from_livre(self, queryset, name, value):
        results = queryset.filter(livre__isnull=not value)
        return results

    class Meta:
        model = Exercice
        fields = ['prefix_prof', 'nom_prof', 'nom_etablissement', 'niveau',
                  'chapitre', 'type', 'livre', 'num_page', 'num_exo', 'is_corrected', 'is_from_livre']

