from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from .models import CountUsageList

@login_required
def count_usage_list(request):
    context = {
        'bmc_count_usage_list': CountUsageList.objects.filter(fac='939')[:50]
    }
    return render(request, 'target/target_list.html', context)