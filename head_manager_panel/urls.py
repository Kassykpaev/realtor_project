from django.urls import path
from .views import (WorkerListView, worker_detail, CreateWorkerView,
                    worker_activate, worker_delete, OptionListView,
                    OptionDeleteView, OptionCreateView, StatusCreateView,
                    StatusListView, StatusDeleteView,)

app_name = 'head_manager_panel'

urlpatterns = [
    path('worker/delete/<int:pk>', worker_delete, name='worker-delete'),
    path('worker/create/activate/<str:sign>/', worker_activate, name='worker-activate'),
    path('workers/create/', CreateWorkerView.as_view(), name='add-worker'),
    path('workers/<int:pk>/', worker_detail, name='worker-detail'),
    path('workers/', WorkerListView.as_view(), name='worker-list'),
    path('options/', OptionListView.as_view(), name='option-list'),
    path('option/create/', OptionCreateView.as_view(), name='option-create'),
    path('option/<int:pk>/delete', OptionDeleteView.as_view(), name='option-delete'),
    path('statuses/', StatusListView.as_view(), name='status-list'),
    path('status/create/', StatusCreateView.as_view(), name='status-create'),
    path('status/<int:pk>/delete', StatusDeleteView.as_view(), name='status-delete'),
]
