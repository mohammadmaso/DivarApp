from .models import Property, Car, ApartmantBuy
import django_filters


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    class Meta:
        model = Car
        fields = ['first_name']