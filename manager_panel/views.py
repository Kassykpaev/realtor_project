import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404 , HttpResponse , FileResponse
from django.shortcuts import render , get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
import datetime

from .forms import WorkerManagerDetailForm , DateRangeForm , WorkerSearch
from main.models import Worker , Lead
from .utilities import get_realtor_statistics , get_manager_statistics , make_excel_file
from realtor_panel.forms import LeadSearchForm


class WorkerListView(LoginRequiredMixin , ListView):
    template_name = 'manager_panel/worker-list.html'
    context_object_name = 'workers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Worker.objects.filter(manager=self.request.user.pk)
        form = WorkerSearch(self.request.GET , queryset=queryset)
        queryset = form.qs
        return queryset

    def get_context_data(self , * , object_list=None , **kwargs):
        context = super(WorkerListView , self).get_context_data(**kwargs)
        context['form'] = WorkerSearch(self.request.GET)
        return context


@login_required
def worker_detail(request , pk):
    worker = get_object_or_404(Worker , pk=pk)
    if worker.manager.pk != request.user.pk:
        raise Http404

    if request.method == "POST":
        form = WorkerManagerDetailForm(request.POST , instance=worker)
        if form.is_valid():
            form.save()
            return reverse('head_manager_panel:worker-detail' , pk=pk)
    else:
        form = WorkerManagerDetailForm(instance=worker)
    context = {'form': form , 'worker': worker}
    return render(request , 'manager_panel/worker-detail.html' , context)


@login_required
def worker_detail_list(request , pk):
    worker = get_object_or_404(Worker , pk=pk)

    if worker.manager.pk != request.user.pk:
        raise Http404

    leads = Lead.objects.filter(worker_id=worker.pk)

    form = LeadSearchForm(request.GET , queryset=leads)

    leads = form.qs

    paginator = Paginator(leads , 10)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'page': page , 'worker': worker , 'leads': page.object_list , 'form': form.form}
    return render(request , 'manager_panel/worker-detail-list.html' , context)


@login_required
def worker_lead_detail(request, pk, id):
    worker = get_object_or_404(Worker, pk=pk)

    if worker.manager.pk != request.user.pk:
        raise Http404

    lead = get_object_or_404(Lead , pk=id)

    if not lead:
        raise Http404

    if lead.worker != worker:
        raise Http404

    context = {'worker': worker , 'lead': lead}
    return render(request, 'manager_panel/worker-lead-detail.html', context)


@login_required
def worker_statistics_realtor(request , pk):
    worker = get_object_or_404(Worker , pk=pk)

    if worker.manager.pk != request.user.pk:
        raise Http404

    context = {}

    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        context = get_realtor_statistics(worker, start_date=start_date, end_date=end_date)
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
    else:
        form = DateRangeForm()
        context['no_date'] = 'lol'
    context['form'] = form
    context['worker'] = worker
    return render(request, 'manager_panel/worker_statistics_realtor.html', context)


@login_required
def worker_statistics_manager(request , pk):
    worker = Worker.objects.get(pk=pk)

    if worker.manager.pk != request.user.pk or not worker.is_manager:
        raise Http404

    context = {}
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        context = get_manager_statistics(worker, start_date=start_date, end_date=end_date)
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
    else:
        form = DateRangeForm()
        context['no_date'] = 'lol'
    context['form'] = form
    context['worker'] = worker
    return render(request, 'manager_panel/worker_statistics_manager.html', context)


@login_required
def worker_statistics(request , pk):
    worker = get_object_or_404(Worker , pk=pk)

    if worker.manager.pk != request.user.pk:
        raise Http404

    context = {'worker': worker}
    return render(request, 'manager_panel/worker_statistics.html', context)


@login_required
def get_workers_statistics(request):
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        make_excel_file(request.user.id, start_date=start_date, end_date=end_date)
        file_path = 'media/statistics.xlsx'
        try:
            response = FileResponse(open(file_path, 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            raise Http404
    else:
        user = Worker.objects.get(id=request.user.id)
        workers = user.worker_set.all()
        context = {}
        if 'start_date' in request.GET and 'end_date' in request.GET:
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            context = get_manager_statistics(user, start_date=start_date, end_date=end_date)
            form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
        else:
            form = DateRangeForm()
            context['no_date'] = 'lol'
        context['form'] = form
        context['workers'] = workers
        return render(request, 'manager_panel/workers_statistics.html', context)
