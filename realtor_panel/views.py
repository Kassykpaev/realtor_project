from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from main.models import Lead, Consumption
from .forms import LeadModelForm, LocationFormset, ConsumptionFormset, LeadSearchForm, AdditionalImageFormset


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'realtor_panel/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 3

    def get_queryset(self):
        queryset = Lead.objects.filter(worker_id=self.request.user.pk)
        form = LeadSearchForm(self.request.GET, queryset=queryset)
        queryset = form.qs.order_by('-date_added')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        context['form'] = LeadSearchForm(self.request.GET)
        return context


@login_required
def add_lead(request):
    if request.method == "POST":
        lead_form = LeadModelForm(request.POST, request.FILES)
        if lead_form.is_valid():
            lead = lead_form.save()
            lead_formset_location = LocationFormset(request.POST, instance=lead)
            hidden_consumption = Consumption.objects.create(lead=lead)
            if lead_formset_location.is_valid():
                lead_formset_location.save()
                hidden_consumption.save()
                messages.add_message(request, messages.SUCCESS, 'New lead created')
                return redirect('realtor_panel:lead-list')
    else:
        lead_form = LeadModelForm(initial={'worker': request.user.pk})
        lead_formset_location = LocationFormset()
    context = {'form': lead_form, 'formset': lead_formset_location}
    return render(request, 'realtor_panel/lead_create.html', context)


@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead_form = LeadModelForm(request.POST, request.FILES, instance=lead)
        if lead_form.is_valid():
            lead_form.save()
            lead_formset_location = LocationFormset(request.POST, instance=lead)
            lead_formset_consumption = ConsumptionFormset(request.POST, instance=lead)
            lead_formset_additional_image = AdditionalImageFormset(request.POST, request.FILES, instance=lead)
            if lead_formset_consumption.is_valid() and lead_formset_location.is_valid():
                lead_formset_location.save()
                lead_formset_consumption.save()
                lead_formset_additional_image.save()
                return redirect('realtor_panel:lead-detail', pk=pk)
    else:
        lead_form = LeadModelForm(instance=lead)
        lead_formset_location = LocationFormset(instance=lead)
        lead_formset_consumption = ConsumptionFormset(instance=lead)
        lead_formset_additional_image = AdditionalImageFormset(instance=lead)
    context = {
        'form': lead_form,
        'formset_location': lead_formset_location,
        'formset_consumption': lead_formset_consumption,
        'formset_additional_image': lead_formset_additional_image,
        'lead': lead,
    }
    return render(request, 'realtor_panel/lead_detail.html', context)


@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        messages.add_message(request, messages.SUCCESS, 'Lead successfully deleted')
        return redirect('realtor_panel:lead-list')
    else:
        context = {'lead': lead}
        return render(request, 'realtor_panel/lead_delete.html', context)
