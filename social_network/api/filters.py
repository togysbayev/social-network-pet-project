from django_filters import rest_framework as filters
from .models import Like

class LikeFilter(filters.FilterSet):
    date_from = filters.DateTimeFilter(field_name='liked_at', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='liked_at', lookup_expr='lte')