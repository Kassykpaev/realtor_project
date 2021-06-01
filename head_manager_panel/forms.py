from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
import django_filters

from main.models import Worker, Option, Status, Coefficient

from .apps import register_worker


class WorkerModelForm(forms.ModelForm):
    manager = forms.ModelChoiceField(queryset=Worker.objects.filter(is_manager=True), label='Manager', required=False)

    class Meta:
        model = Worker
        fields = (
            'username', 'first_name',
            'last_name', 'email',
            'phone', 'age',
            'gender', 'is_realtor',
            'is_manager', 'is_head_manager',
            'manager', 'date_joined',
        )


class WorkerCreateModelForm(forms.ModelForm):
    manager = forms.ModelChoiceField(queryset=Worker.objects.filter(is_manager=True), label='Manager', required=False)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password (repeat)', widget=forms.PasswordInput,
                                help_text="Enter the same password for check")

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            print('valid: ' + password1)
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        password1 = self.data.get('password1')
        password2 = self.cleaned_data['password2']
        print(password1)
        print('123')
        if password1 and password2 and password2 != password1:
            errors = {'password2': ValidationError(
                "Entered passwords don't match", code='password_mismatch'
            )}
            raise ValidationError(errors)
        super().clean()

    def save(self, commit=True):
        worker = super(WorkerCreateModelForm, self).save(commit=False)
        worker.set_password(self.cleaned_data['password1'])
        worker.is_active = False
        if commit:
            worker.save()

        register_worker.send(WorkerCreateModelForm, instance=worker)
        return worker

    class Meta:
        model = Worker
        fields = (
            'username', 'password1', 'password2',
            'first_name',
            'last_name', 'email',
            'phone', 'age',
            'gender', 'is_realtor',
            'is_manager', 'is_head_manager',
            'manager',
        )


class UserSearchForm(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    manager = django_filters.CharFilter(field_name='manager', lookup_expr='icontains')
    # is_active = django_filters.ChoiceFilter(field_name='is_active', )

    class Meta:
        model = Worker
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'manager', 'is_active')
        exclude = ['image', ]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = '__all__'


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'
