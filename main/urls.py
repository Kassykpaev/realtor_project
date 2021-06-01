from django.urls import path
from .views import (WorkerLoginView, WorkerLogoutView, profile, WorkerChangePasswordView,
                    WorkerResetPasswordDoneView, WorkerResetPasswordView, WorkerResetPasswordConfirmView,
                    WorkerResetPasswordCompleteView, index, get_statistics, realtor_statistics,
                    manager_statistics)

app_name = 'main'

urlpatterns = [
    path('accounts/login/', WorkerLoginView.as_view(), name='login'),
    path('accounts/logout/', WorkerLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/password/change', WorkerChangePasswordView.as_view(), name='password_change'),
    path('statistics/manager/', realtor_statistics, name='realtor-statistics'),
    path('statistics/realtor/', manager_statistics, name='manager-statistics'),
    path('statistics/', get_statistics, name='statistics'),
    path('reset_password/', WorkerResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_sent/', WorkerResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', WorkerResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', WorkerResetPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('', index, name='index'),
]