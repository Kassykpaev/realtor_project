from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_path
import realtor_project.settings as settings


class Coefficient(models.Model):
    name = models.CharField(max_length=255, verbose_name='Coefficient name')
    coefficient = models.FloatField(verbose_name='Coefficient')


def get_coefficient(coefficient):
    c = Coefficient.objects.get(name=coefficient)
    return c.coefficient


class Worker(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email', db_index=True)
    phone = models.CharField(max_length=11, unique=True, verbose_name='Phone number', db_index=True)
    age = models.IntegerField(verbose_name='Age', null=True)
    gender = models.CharField(max_length=255, verbose_name='Gender')
    is_realtor = models.BooleanField(default=True, verbose_name='Realtor')
    is_manager = models.BooleanField(default=False, verbose_name='Promote to manager')
    is_head_manager = models.BooleanField(default=False, verbose_name='Promote to head manager')
    manager = models.ForeignKey('Worker', on_delete=models.PROTECT, verbose_name='Manager', null=True)
    image = models.ImageField(verbose_name='Image', upload_to=get_path, blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = 'Workers'
        verbose_name = 'Worker'
        ordering = ['-date_joined', ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def delete(self, *args, **kwargs):
        if self.is_manager:
            for worker in self.worker_set.all():
                worker.manager = None
                worker.save()
        for lead in self.lead_set.all():
            lead.delete()
        super(Worker, self).delete(*args, **kwargs)


class Option(models.Model):
    name = models.CharField(max_length=255, verbose_name='Option name')

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name='Status name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Statuses'
        verbose_name = 'Status'


class Lead(models.Model):
    name = models.CharField(max_length=255, verbose_name='Lead name')
    phone = models.CharField(max_length=11, verbose_name='Phone number')
    email = models.CharField(max_length=255, verbose_name='Email', null=True, blank=True)
    option = models.ForeignKey(Option, on_delete=models.PROTECT, verbose_name='Option')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Status', null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, verbose_name='Current realtor')
    start_price = models.BigIntegerField(verbose_name='Start price', null=True, blank=True)
    date_added = models.DateField(auto_now_add=True, verbose_name='Added day')
    percent = models.FloatField(verbose_name='Income percent', default=settings.PERCENT)
    company_percent = models.FloatField(verbose_name='Company percent', default=settings.COMPANY_PERCENT)
    deal_value = models.IntegerField(verbose_name='Deal cost', default=0)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    image = models.ImageField(verbose_name='Image', upload_to=get_path, blank=True, null=True, default=None)
    date_closed = models.DateField(null=True, blank=True, verbose_name='Date closed')

    class Meta:
        ordering = ['-date_added', ]

    def __str__(self):
        return f'{self.name} - {self.option}'

    def delete(self, *args, **kwargs):
        for cons in self.consumption_set.all():
            cons.delete()
        if hasattr(self, 'location'):
            self.location.delete()
        for ai in self.additionalimage_set.all():
            ai.delete()
        super(Lead, self).delete(*args, **kwargs)


class Consumption(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Lead', null=True, blank=True)
    description = models.TextField(verbose_name='Consumption name', null=True, blank=True)
    cost = models.IntegerField(verbose_name='Cost', null=True, blank=True)

    def __str__(self):
        return f'{self.lead} - {self.description}:{self.cost}'


class Location(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, verbose_name='Lead')
    locality = models.CharField(verbose_name='Locality', max_length=255, null=True, blank=True)
    district = models.CharField(verbose_name='District', max_length=255, null=True, blank=True)
    main_street = models.CharField(verbose_name='Main street', max_length=255, null=True, blank=True)
    secondary_street = models.CharField(verbose_name='Secondary street', max_length=255, null=True, blank=True)
    house_number = models.CharField(verbose_name='House number', max_length=20, null=True, blank=True)
    apartment_number = models.CharField(verbose_name='Apartment number', max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.locality}'


class AdditionalImage(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Lead', null=True, blank=True)
    image = models.ImageField(upload_to=get_path, verbose_name='Image', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Additional images'
        verbose_name = 'Additional image'
