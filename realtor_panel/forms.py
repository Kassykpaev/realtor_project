import django_filters

from django import forms

from main.models import Lead, Location, Consumption, AdditionalImage


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'name', 'phone',
            'email', 'option',
            'status', 'description',
            'worker', 'image',
            'percent', 'deal_value',
            'company_percent', 'date_closed'
        )
        widgets = {'worker': forms.HiddenInput, 'date_closed': forms.HiddenInput}


LocationFormset = forms.inlineformset_factory(Lead, Location, fields=('locality', 'district', 'main_street', 'secondary_street', 'house_number', 'apartment_number'))
ConsumptionFormset = forms.inlineformset_factory(Lead, Consumption, fields=('description', 'cost'))
AdditionalImageFormset = forms.inlineformset_factory(Lead, AdditionalImage, fields='__all__')


class LeadSearchForm(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    deal_value_gt = django_filters.NumberFilter(field_name='deal_value', lookup_expr='gte')
    deal_value_lt = django_filters.NumberFilter(field_name='deal_value', lookup_expr='lte')

    class Meta:
        model = Lead
        fields = (
            'name', 'phone',
            'email', 'option',
            'status', 'description',
            'deal_value',
        )
