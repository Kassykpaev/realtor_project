from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from main.models import Worker
from manager_panel.forms import DateRangeForm
from manager_panel.utilities import get_realtor_statistics, get_manager_statistics


def index(request):
    return redirect('main:login')


class WorkerLoginView(LoginView):
    template_name = 'main/login.html'


class WorkerLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


@login_required
def profile(request):
    user = request.user
    user = Worker.objects.get(id=user.id)
    print(user.image)
    context = {
        'user': user,
    }
    return render(request, 'main/profile.html', context)


class WorkerChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    success_message = 'You successfully changed your password'
    success_url = reverse_lazy('main:profile')
    template_name = 'main/password-change.html'


class WorkerResetPasswordView(PasswordResetView):
    template_name = 'main/reset_password.html'
    email_template_name = 'main/reset_password_email.html'
    success_url = reverse_lazy('main:password_reset_done')


class WorkerResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'main/reset_password_done.html'


class WorkerResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'main/reset_password_confirm.html'

    success_url = reverse_lazy('main:password_reset_complete')


class WorkerResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'main/reset_password_complete.html'


@login_required
def get_statistics(request):
    return render(request, 'main/statistics.html')


@login_required
def realtor_statistics(request):
    context = {}

    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        context = get_realtor_statistics(request.user, start_date=start_date, end_date=end_date)
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
    else:
        form = DateRangeForm()
        context['no_date'] = 'lol'
    context['form'] = form

    return render(request, 'main/statistics_realtor.html', context)


@login_required
def manager_statistics(request):
    if not request.user.is_manager:
        raise Http404

    context = {}
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        context = get_manager_statistics(request.user, start_date=start_date, end_date=end_date)
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
    else:
        form = DateRangeForm()
        context['no_date'] = 'lol'
    context['form'] = form
    return render(request, 'main/statistics_manager.html', context)
