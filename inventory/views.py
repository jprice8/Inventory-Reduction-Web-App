from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from .models import Invcount 
from target.models import CountUsageList

def index(request):
    return render(request, 'inventory/landing.html')

# Inventory views
@login_required
def inventory_list(request):
    context = {
        'bmc_count_usage_list': CountUsageList.objects.filter(fac='939')[:50]
    }
    return render(request, 'inventory/inventory_list.html', context)
