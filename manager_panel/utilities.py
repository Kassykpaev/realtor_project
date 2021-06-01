import datetime
import xlsxwriter
from django.http import Http404
from django.shortcuts import get_object_or_404

from main.models import Lead, Worker, Coefficient


def validate_date(start_date, end_date):
    add_hour = ' 00:00:00'

    if type(end_date) == str:
        end_date += add_hour
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    if type(start_date) == str:
        start_date += add_hour
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

    return start_date, end_date


def get_realtor_statistics(worker, start_date, end_date):
    context = {}
    print(type(end_date))
    print(type(start_date))

    start_date, end_date = validate_date(start_date, end_date)

    print(type(end_date))
    print(type(start_date))

    end_date = end_date + datetime.timedelta(days=1)

    if start_date > end_date:
        raise context

    queryset = Lead.objects.filter(worker=worker, date_added__range=[start_date, end_date])

    context['leads_count'] = len(queryset)
    context['income'] = 0
    context['company_income'] = 0
    for lead in queryset.filter(status__name='Successful close'):
        tmp = lead.percent * lead.deal_value
        context['company_income'] += tmp * lead.company_percent
        print(lead.consumption_set.all())
        for cons in lead.consumption_set.all():
            if cons.cost is None:
                continue
            else:
                tmp -= cons.cost
        context['income'] += tmp

    context['leads_closed_successfully'] = len(queryset.filter(status__name='Successful close'))
    context['leads_closed_unsuccessfully'] = len(queryset.filter(status__name='Unsuccessful close'))
    context['leads_in_progress'] = context['leads_count'] - context['leads_closed_successfully'] - context['leads_closed_unsuccessfully']
    return context


def get_manager_statistics(worker, start_date, end_date):
    context = {}
    start_date, end_date = validate_date(start_date, end_date)

    end_date = end_date + datetime.timedelta(days=1)

    if end_date < start_date or not worker.is_manager:
        return context

    context['leads_closed_successfully'] = 0
    context['leads_closed_unsuccessfully'] = 0
    context['leads_in_progress'] = 0
    context['company_income'] = 0

    for realtor in worker.worker_set.all():
        if realtor.is_realtor:
            tmp = get_realtor_statistics(realtor, start_date, end_date)
            print(tmp)
            context['leads_closed_successfully'] += tmp['leads_closed_successfully']
            context['leads_closed_unsuccessfully'] += tmp['leads_closed_unsuccessfully']
            context['leads_in_progress'] += tmp['leads_in_progress']
            context['company_income'] += tmp['company_income']

    worker_count = len(worker.worker_set.all()) if len(worker.worker_set.all()) != 0 else 1
    context['leads_closed_successfully_avg'] = context['leads_closed_successfully'] * 1.0 / worker_count
    context['leads_closed_unsuccessfully_avg'] = context['leads_closed_unsuccessfully'] * 1.0 / worker_count
    context['company_income_avg'] = context['company_income'] * 1.0 / worker_count
    return context


def decorate_realtor(worker, sheet, sdate, edate):
    k = 0
    statistics = get_realtor_statistics(worker, sdate, edate)
    for (i, statistic) in enumerate(statistics):
        sheet.write(i, 0, statistic)
        sheet.write(i, 1, statistics[statistic])
    k = len(statistics)
    k += 3
    return k


def decorate_manager(beg, worker, sheet, sdate, edate):
    statistics = get_manager_statistics(worker, sdate, edate)
    for (i, statistic) in enumerate(statistics):
        sheet.write(beg + i, 0, statistic)
        sheet.write(beg + i, 1, statistics[statistic])


def decorate_sheet(worker, sheet, sdate, edate):
    k = 0
    if worker.is_realtor:
        k = decorate_realtor(worker, sheet, sdate, edate)
    if worker.is_manager:
        decorate_manager(k, worker, sheet, sdate, edate)


def make_excel_file(manager_id, start_date, end_date):
    manager = get_object_or_404(Worker, pk=manager_id)
    if not manager.is_manager:
        raise Http404

    workers = manager.worker_set.all()
    path = 'media/statistics.xlsx'
    work_book = xlsxwriter.Workbook(path)
    for worker in workers:
        new_sheet = work_book.add_worksheet()
        decorate_sheet(worker, new_sheet, start_date, end_date)

    work_book.close()


def get_kpi(worker, now=None):
    if now is None:
        now = datetime.datetime.now()
    month_start = datetime.datetime(now.year, now.month, 1)
    queryset = Lead.objects.filter(worker=worker, date_added__range=[month_start, now], status__name='Successful close')
    goal = Coefficient.objects.get(name='Goal')
    goal = goal if goal != 0 else 1
    kpi = 100 * (len(queryset)*1.0/int(goal))
    return kpi
