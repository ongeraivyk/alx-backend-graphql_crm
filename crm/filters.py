import django_filters
from .models import Customer, Product, Order
from django.db.models import Q

# --------------------------
# CUSTOMER FILTER
# --------------------------
class CustomerFilter(django_filters.FilterSet):
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email_icontains = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    created_at_gte = django_filters.DateFilter(field_name='id', lookup_expr='gte')  # Assuming id as created_at proxy
    created_at_lte = django_filters.DateFilter(field_name='id', lookup_expr='lte')
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')

    class Meta:
        model = Customer
        fields = ['name_icontains', 'email_icontains', 'created_at_gte', 'created_at_lte', 'phone_pattern']

    def filter_phone_pattern(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)


# --------------------------
# PRODUCT FILTER
# --------------------------
class ProductFilter(django_filters.FilterSet):
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    stock_gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name_icontains', 'price_gte', 'price_lte', 'stock_gte', 'stock_lte']


# --------------------------
# ORDER FILTER
# --------------------------
class OrderFilter(django_filters.FilterSet):
    total_amount_gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name = django_filters.CharFilter(method='filter_product_name')

    class Meta:
        model = Order
        fields = ['total_amount_gte', 'total_amount_lte', 'customer_name', 'product_name']

    def filter_product_name(self, queryset, name, value):
        return queryset.filter(products__name__icontains=value).distinct()
