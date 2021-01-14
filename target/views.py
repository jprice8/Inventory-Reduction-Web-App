from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from .models import CountUsageList
from inventory.models import Facility

@login_required
def count_usage_list(request):
    dmm = Facility.objects.filter(dmm=request.user)[0]

    context = {
        'bmc_count_usage_list': CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            issue_qty=0
        ).filter(
            po_qty=0
        ).filter(
            count_qty__gt=0
        ).order_by(
            '-default_uom_price'
        )
    }
    return render(request, 'target/target_list.html', context)
