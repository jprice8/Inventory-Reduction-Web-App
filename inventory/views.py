from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User

from .models import Invcount, Facility
from target.models import CountUsageList

def index(request):
    return render(request, 'inventory/landing.html')

# Inventory views
@login_required
def inventory_list(request):

    dmm = Facility.objects.filter(dmm=request.user)[0]
    
    context = {
        'count_usage_list': CountUsageList.objects.filter(fac=dmm.fac)[:500],
        'dmm': dmm,
    }
    return render(request, 'inventory/inventory_list.html', context)
