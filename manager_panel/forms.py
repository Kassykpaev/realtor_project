from django import forms
from main.models import Worker, Lead
import django_filters


class WorkerManagerDetailForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            'username', 'first_name',
            'last_name', 'email',
            'phone', 'age',
            'gender', 'date_joined',
        )


class WorkerSearch(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = Worker
        fields = ('username', 'first_name', 'last_name', 'phone', 'email')


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start date')
    end_date = forms.DateField(label='End date')
