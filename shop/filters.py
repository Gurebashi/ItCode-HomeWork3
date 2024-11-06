from cProfile import label

import django_filters
from django.db.models import Q
from django_filters import RangeFilter
from django_filters import OrderingFilter
import shop.models


class Picture(django_filters.FilterSet):
    price_range = django_filters.RangeFilter(field_name='price', label='Цены от и до')
    title = django_filters.CharFilter(label='Название картины', lookup_expr='icontains')
    availability = django_filters.BooleanFilter(label="В наличии", method='filter_availability')
    original = django_filters.BooleanFilter(label="Оригинал", method="filter_original")
    public_data_range = django_filters.DateFromToRangeFilter(field_name='public_date', label='Год картины от и до')
    term = django_filters.CharFilter(method='filter_term', label="Поиск по критериям")
    style_category_union = django_filters.CharFilter(method='filter_stylecat', label='Сочетание жанра и стиля')
    order_by = django_filters.OrderingFilter(fields=(('price', 'price'),('-price', '-price'),),label='Сортировка по цене',choices=[('price', 'По возрастанию'),
        ('-price', 'По убыванию'),
    ]
)
    class Meta:
        model = shop.models.Picture
        fields = ['title', 'author', 'category', 'style']

    def filter_availability(self, queryset, name, value):
        if value:
            return queryset.filter(availability=True)
        return queryset.filter(availability=False)

    def filter_original(self, queryset, name, value):
        if value:
            return queryset.filter(is_original=True)
        return queryset.filter(is_original=False)

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(title__icontains=term) | Q(author__last_name__icontains=term) | Q(
                author__first_name__icontains=term) | Q(history__icontains=term)
        return queryset.filter(criteria).distinct()

    def filter_stylecat(selfself, queryset, name,
                        value):  ##Функция для создания фильтра по поиску картин с определенным пейзажем и определенным жанром
        stylecategory = Q()
        for union in value.split():
            stylecategory &= Q(style__style_name__icontains=union) | Q(category__category_name__icontains=union)
        return queryset.filter(stylecategory).distinct()
