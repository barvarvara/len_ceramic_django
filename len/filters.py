import django_filters.widgets
from django.forms import DateInput, TimeInput
from django_filters import FilterSet, CharFilter, DateFilter, TimeFilter

from len.models import Clients, Contacts, Classes


class ContactFilter(FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains', label='Имя')
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains', label='Фамилия')
    middle_name = CharFilter(field_name='middle_name', lookup_expr='icontains', label='Отчество')

    class Meta:
        model = Contacts
        fields = ('first_name', 'last_name', 'middle_name', 'phone')


class ClassFilter(FilterSet):
    date = DateFilter(field_name='date', widget=DateInput(attrs={'type': 'date', 'class': 'form-control',}))
    time = TimeFilter(field_name='time', widget=TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    class Meta:
        model = Classes
        fields = ('class_type', 'date', 'time')


class ClientFilter(FilterSet):
    fcs = CharFilter(field_name='fcs', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Clients
        fields = ('name', 'fcs', 'client_status', 'client_type')
