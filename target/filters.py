import django_filters

from .models import CountUsageList


class ItemFilter(django_filters.FilterSet):
    imms = django_filters.CharFilter(field_name='imms', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = CountUsageList
        fields = ['imms', 'description']