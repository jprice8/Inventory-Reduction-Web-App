from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator

import os

from .models import Invcount, Facility
from target.models import CountUsageList
from target.filters import ItemFilter

def index(request):
    return render(request, 'inventory/landing.html')

# Inventory views
@login_required
def inventory_list(request):
    debug = os.environ.get("DJANGO_DEBUG", False)
    matching_facility = Facility.objects.filter(dmm=request.user)

    if matching_facility.exists():
        dmm = Facility.objects.filter(dmm=request.user)[0]
    else:
        return render(request, 'inventory/non_dmm_redir.html')

    sliced_qs = CountUsageList.objects.filter(
        fac=dmm.fac
    ).filter(
        isTarget=False
    ).exclude(
        issue_qty=0, luom_po_qty=0
    ).values_list(
        'id', flat=True
    )[:100]

    # make a copy so we can filter the qs
    intake_list = CountUsageList.objects.filter(id__in=sliced_qs)

    # django-filter our queryset
    item_filter = ItemFilter(request.GET, queryset=intake_list)

    # built in pagination
    paginator = Paginator(item_filter.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': item_filter,
        'dmm': dmm,
        'DEBUG': debug,
        'page_obj': page_obj,
    }

    return render(request, 'inventory/inventory_list.html', context)

# View docs
def view_docs(request):
    return render(request, 'inventory/docs.html')

# Redirect non-dmms
def non_dmm_redirect(request):
    return render(request, 'inventory/non_dmm_redir.html')