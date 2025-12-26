import django_filters
from .models import Complaint

class ComplaintFilter(django_filters.FilterSet):
    urgency_min = django_filters.NumberFilter(field_name='urgency_score', lookup_expr='gte')
    urgency_max = django_filters.NumberFilter(field_name='urgency_score', lookup_expr='lte')
    category = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Complaint
        fields = ['category', 'status', 'urgency_min', 'urgency_max']
