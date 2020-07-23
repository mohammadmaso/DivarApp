from .models import Property, Car, ApartmantBuy
import django_filters


class CarFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()


    class Meta:
        model = Car
        fields = ['sell_choice', 'price', 'is_exchange', 'function' , 'is_immediate' ,'zone', 'pub_date', ]