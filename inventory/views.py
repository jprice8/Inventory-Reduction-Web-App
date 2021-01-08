from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from .models import Invcount, CountUsageList

def index(request):
    return render(request, 'inventory/landing.html')

# Inventory views
@login_required
def inventory_list(request):
    context = {
        'inventory_list': Invcount.objects.all()[:50]
    }
    return render(request, 'inventory/inventory_list.html', context)

@login_required
def count_usage_list(request):
    context = {
        'bmc_count_usage_list': CountUsageList.objects.filter(fac='939')[:50]
    }
    return render(request, 'inventory/reduction_list.html', context)