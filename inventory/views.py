from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User

import os

from .models import Invcount, Facility
from target.models import CountUsageList

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

    context = {
        'count_usage_list': CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            isTarget=False
        ).exclude(
            issue_qty=0, luom_po_qty=0
        )[:100],
        'dmm': dmm,
        'DEBUG': debug,
    }

    return render(request, 'inventory/inventory_list.html', context)

# View docs
def view_docs(request):
    return render(request, 'inventory/docs.html')

# Redirect non-dmms
def non_dmm_redirect(request):
    return render(request, 'inventory/non_dmm_redir.html')