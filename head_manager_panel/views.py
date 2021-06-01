from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DeleteView, UpdateView
from main.models import Worker, Option, Status, Coefficient
from .forms import WorkerModelForm, WorkerCreateModelForm, UserSearchForm, OptionForm, StatusForm
from .utilities import signer


class WorkerListView(LoginRequiredMixin, ListView):
    template_name = 'head_manager_panel/workers_list.html'
    context_object_name = 'workers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = UserSearchForm(self.request.GET, queryset=queryset)
        queryset = form.qs
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        context['form'] = UserSearchForm(self.request.GET)
        return context


@login_required
def worker_detail(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    if request.method == "POST":
        form = WorkerModelForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('head_manager_panel:worker-detail', pk=pk)
    else:
        form = WorkerModelForm(instance=worker)
    context = {'form': form, 'worker': worker}
    return render(request, 'head_manager_panel/worker_detail.html', context)


class CreateWorkerView(LoginRequiredMixin, CreateView):
    template_name = 'head_manager_panel/create_worker.html'
    model = Worker
    form_class = WorkerCreateModelForm
    success_url = reverse_lazy('head_manager_panel:worker-list')


@login_required
def worker_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/invalid_signature.html')
    worker = get_object_or_404(Worker, username=username)

    if worker.is_active:
        return render(request, 'main/worker_already_activated.html')
    else:
        worker.is_active = True
        worker.save()
        return render(request, 'main/worker_activation_done.html')


@login_required
def worker_delete(request, pk):
    worker = get_object_or_404(Worker, pk=pk)

    if request.method == "POST":
        worker.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted')
        return redirect('head_manager_panel:worker-list')
    else:
        context = {'worker': worker}
        return render(request, 'head_manager_panel/delete_worker.html', context)


class OptionListView(LoginRequiredMixin, ListView):
    template_name = 'head_manager_panel/option_list.html'
    context_object_name = 'options'

    def get_queryset(self):
        return Option.objects.all()


class OptionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'head_manager_panel/option_delete.html'
    context_object_name = 'option'

    def get_queryset(self):
        return Option.objects.all()

    def get_success_url(self):
        return reverse('head_manager_panel:option-list')


class OptionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'head_manager_panel/option_create.html'
    model = Option
    form_class = OptionForm

    def get_success_url(self):
        return reverse('head_manager_panel:option-list')


class StatusListView(LoginRequiredMixin, ListView):
    template_name = 'head_manager_panel/status_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all()


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'head_manager_panel/status_delete.html'
    context_object_name = 'status'

    def get_queryset(self):
        return Status.objects.all()

    def get_success_url(self):
        return reverse('head_manager_panel:status-list')


class StatusCreateView(LoginRequiredMixin, CreateView):
    template_name = 'head_manager_panel/status_create.html'
    model = Status
    form_class = StatusForm

    def get_success_url(self):
        return reverse('head_manager_panel:status-list')
