from django.urls import path
from .views import (WorkerListView, worker_detail, worker_detail_list,
                    worker_lead_detail, worker_statistics, worker_statistics_realtor,
                    worker_statistics_manager, get_workers_statistics)


app_name = 'manager_panel'

urlpatterns = [
    path('worker/<int:pk>/statistics/realtor/', worker_statistics_realtor, name='worker-statistics-realtor'),
    path('worker/<int:pk>/statistics/manager/', worker_statistics_manager, name='worker-statistics-manager'),
    path('worker/<int:pk>/statistics/', worker_statistics, name='worker-statistics'),
    path('workers/<int:pk>/leads/<int:id>', worker_lead_detail, name='worker-lead-detail'),
    path('worker/<int:pk>/leads/', worker_detail_list, name='worker-lead-list'),
    path('worker/<int:pk>', worker_detail, name='worker-detail'),
    path('workers/', WorkerListView.as_view(), name='workers-list'),
    path('workers/statics/', get_workers_statistics, name='all-workers-statistics')
]
