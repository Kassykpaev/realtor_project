from django.urls import path
from .views import add_lead, LeadListView, lead_detail, lead_delete

app_name = 'realtor_panel'

urlpatterns = [
    path('lead/create/', add_lead, name='create-lead'),
    path('lead/delete/<int:pk>/', lead_delete, name='lead-delete'),
    path('lead/<int:pk>/', lead_detail, name='lead-detail'),
    path('', LeadListView.as_view(), name='lead-list')
]
