from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Sum
from django.http import JsonResponse

from inventory.models import Facility
from target.models import CountUsageList, MovementPlan

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
        luom_po_qty=0
    ).filter(
        isTarget=False
    ).aggregate(Sum('ext_cost'))

    # total ext cost of targeted items
    total_target = CountUsageList.objects.filter(
        fac=dmm.fac
    ).filter(
        issue_qty=0
    ).filter(
        luom_po_qty=0
    ).filter(
        isTarget=True
    ).aggregate(Sum('ext_cost'))

    # total movement plan ext for action of not 0
    completed_plans = MovementPlan.objects.filter(
        dmm=request.user
    ).exclude(
        result=MovementPlan.Result.outstanding
    )

    # get completed ext for items reduced
    completed_ext = 0
    for plan in completed_plans:
        completed_ext += plan.accepted_qty * plan.item.wt_avg_cost

    # get all plans dmm has accepted
    accepted_plans = MovementPlan.objects.filter(
        ship_fac=dmm.fac
    ).filter(
        result=MovementPlan.Result.accepted
    )

    # get accepted ext for items moving to dmm facility
    accepted_ext = 0
    for plan in accepted_plans:
        accepted_ext += plan.accepted_qty * plan.item.wt_avg_cost

    # all movement plans with the user's facility listed as desired destination
    my_plans = MovementPlan.objects.filter(
        ship_fac=dmm.fac
    ).filter(
        result=MovementPlan.Result.outstanding
    )

    context = {
        'facility': dmm,
        'no_move_ext': total_no_move['ext_cost__sum'],
        'target_ext': total_target['ext_cost__sum'],
        'completed_ext': completed_ext,
        'accepted_ext': accepted_ext,
        'plans': my_plans,
    }

    return render(request, 'act/act_page.html', context)

# Dmm accept or reject request to move units to their facility
@login_required
@ensure_csrf_cookie
def result_handler(request, pk):
    dmm_response = request.POST['action']

    if request.method == 'POST':
        plan_from_id = get_object_or_404(MovementPlan, pk=pk)
        result_before = plan_from_id.result
        if dmm_response == 'accepted':
            plan_from_id.result = MovementPlan.Result.accepted
            plan_from_id.save(update_fields=['result'])
            result_after = plan_from_id.result
        elif dmm_response == 'rejected':
            plan_from_id.result = MovementPlan.Result.rejected
            plan_from_id.save(update_fields=['result'])
            result_after = plan_from_id.result
        else:
            result_after = 'error'

        response_data = {
            'django_response': f'plan had result of... {result_before} and is now... {result_after}'
        }
    else:
        response_data = {
            'django_response': f'Invalid request: resend as POST'
        }

    return JsonResponse(response_data)

# Dmm has accepted the request, now set the accepted quantity
@login_required
@ensure_csrf_cookie
def accept_qty_handler(request, pk):
    dmm_accept_qty = request.POST['accept_qty']
    print(dmm_accept_qty)

    if request.method == 'POST':
        plan_from_id = get_object_or_404(MovementPlan, pk=pk)
        accept_qty_before = plan_from_id.accepted_qty
        plan_from_id.accepted_qty = dmm_accept_qty
        plan_from_id.save(update_fields=['accepted_qty'])
        accept_qty_after = plan_from_id.accepted_qty
    
    response_data = {
        'django_response': f'plan had accepted qty of... {accept_qty_before} and is now {accept_qty_after}'
    }

    return JsonResponse(response_data)

@login_required
def review_accepted(request):
    # facility of requesting dmm
    dmm = Facility.objects.filter(dmm=request.user)[0]

    accepted_plans = MovementPlan.objects.filter(
        ship_fac=dmm.fac
    ).filter(
        result=MovementPlan.Result.accepted
    )

    context = {
        'accepted_plans': accepted_plans,
    }

    return render(request, 'act/review_accepted.html', context)
    

