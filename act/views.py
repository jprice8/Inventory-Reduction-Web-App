from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from inventory.models import Facility
from target.models import CountUsageList

@login_required
def act_page(request):
    # facility of requesting dmm
    dmm = Facility.objects.filter(dmm=request.user)[0]
    # total ext cost of no move at dmm's facility
    total_no_move = CountUsageList.objects.filter(
        fac=dmm.fac
    ).filter(
        issue_qty=0
    ).filter(
        po_qty=0
    ).aggregate(Sum('ext_cost'))

    context = {
        'facility': dmm.fac,
        'no_move': total_no_move['ext_cost__sum'],
    }

    return render(request, 'act/act_page.html', context)