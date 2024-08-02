import django_filters
from .models import Ticket
from django import forms


class TicketFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    event_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Ticket
        fields = ('price__gt', 'price__lt', 'event_date')

