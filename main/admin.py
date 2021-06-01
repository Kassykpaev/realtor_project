from django.contrib import admin

from .models import Worker, Option, Status, Lead, Location, Consumption, AdditionalImage, Coefficient


class WorkerAdmin(admin.ModelAdmin):
    search_fields = (('first_name', 'last_name'), 'phone')
    list_display = (
        'username', 'first_name', 'last_name',
    )
    fields = (
        ('username', 'password'),
        ('first_name', 'last_name'),
        ('email', 'phone'), 'age',
        'gender', 'is_realtor',
        ('is_manager', 'is_head_manager'),
        'manager', 'last_login', 'date_joined', 'image',
    )
    readonly_fields = ('last_login', 'date_joined',)


class OptionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LocationTabular(admin.TabularInline):
    model = Location


class ConsumptionTabular(admin.TabularInline):
    model = Consumption


class AdditionalImageTabular(admin.TabularInline):
    model = AdditionalImage


class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone'
    )
    fields = (
        'name', 'phone',
        'email', 'option',
        ('status', 'worker'),
        ('max_price', 'min_price'),
        'date_added', 'percent', 'deal_value', 'company_percent', 'image',
    )
    readonly_fields = ('date_added', )
    inlines = (LocationTabular, ConsumptionTabular, AdditionalImageTabular)


class LocationAdmin(admin.ModelAdmin):
    fields = ('district', 'locality', 'lead', 'main_street', 'secondary_street', 'house_number', 'apartment_number')
    list_display = ('district', 'locality')


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Coefficient)
