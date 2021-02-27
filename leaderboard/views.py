from django.shortcuts import render

from target.models import MovementPlan
from inventory.models import Facility

def leaderboard(request):
    dmms = Facility.objects.all()
    dmm_list = []
    for d in dmms:
        dmm_list.append(d.dmm.username)

    # Get total plans
    dmm_total_plans = []
    for d in dmm_list:
        plans = 0
        for i in MovementPlan.objects.all():
            if d == i.dmm.username:
                plans += 1

        dmm_total_plans.append(plans)

    # Get finalized plans
    finalized_plans = MovementPlan.objects.filter(
        isFinalized=True
    )
    dmm_finalized_plans = []
    for d in dmm_list:
        plans = 0
        for i in finalized_plans:
            if d == i.dmm.username:
                plans += 1
        dmm_finalized_plans.append(plans)

    # Get total dollar amount removed
    dmm_total_reduced = []
    for d in dmm_list:
        reduced = 0
        for i in finalized_plans:
            if d == i.dmm.username:
                reduced += i.accepted_qty * i.item.luom_cost
        dmm_total_reduced.append(reduced)

    # zip all stats together and sort them by highest reduction amount
    dmm_data = sorted(zip(dmm_list, dmm_total_plans, dmm_finalized_plans, dmm_total_reduced), key=lambda x: x[3], reverse=True)

    context = {
        'dmm_data': dmm_data,
    }

    return render(request, 'leaderboard/leaderboard.html', context)