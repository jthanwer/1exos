from rest_framework import generics
from django_filters import rest_framework as filters
from django.db.models import Count
from .models import Exercice


class ExerciceFilter(filters.FilterSet):
    posteur__nom_prof = filters.CharFilter(lookup_expr='icontains')
    is_corrected = filters.BooleanFilter(field_name='corrections', method='filter_is_corrected')

    def filter_is_corrected(self, queryset, name, value):
        if value:
            results = queryset.annotate(num_c=Count(name)).filter(num_c__gte=1)
        else:
            results = queryset.annotate(num_c=Count(name)).filter(num_c__lte=0)
        return results

    class Meta:
        model = Exercice
        fields = ['posteur__classe', 'posteur__nom_prof', 'posteur__etablissement',
                  'category', 'type', 'livre', 'num_page', 'num_exo', 'is_corrected']

