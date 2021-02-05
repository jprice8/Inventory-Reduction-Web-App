from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Sum
from django.http import JsonResponse

from inventory.models import Facility
from target.models import CountUsageList, MovementPlan

from excel_response import ExcelResponse

import datetime as dt
import os

@login_required
def act_page(request):
    debug = os.environ.get("DJANGO_DEBUG", False)
    matching_facility = Facility.objects.filter(dmm=request.user)
    
    if matching_facility.exists():
        # facility of requesting dmm
        dmm = Facility.objects.filter(dmm=request.user)[0]
    else:
        return render(request, 'inventory/non_dmm_redir.html')

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
        completed_ext += plan.accepted_qty * plan.item.luom_cost

    # get all plans dmm has accepted
    accepted_plans = MovementPlan.objects.filter(
        ship_fac=dmm.fac
    ).filter(
        result=MovementPlan.Result.accepted
    )

    # get accepted ext for items moving to dmm facility
    accepted_ext = 0
    for plan in accepted_plans:
        accepted_ext += plan.accepted_qty * plan.item.luom_cost

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
        'DEBUG': debug,
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

@login_required
def review_completed(request):
    # facility of requesting dmm
    dmm = Facility.objects.filter(dmm=request.user)[0]

    completed_plans = MovementPlan.objects.filter(
        dmm=request.user
    ).filter(
        result=MovementPlan.Result.accepted
    )

    context = {
        'completed_plans': completed_plans,
    }

    return render(request, 'act/review_completed.html', context)

@login_required
def accepted_export_excel(request):
    # facility of requesting dmm
    dmm = Facility.objects.filter(dmm=request.user)[0]

    # get the date for the output filename
    t_day = dt.datetime.today().day
    t_month = dt.datetime.today().month
    t_year = dt.datetime.today().year

    # queryset of plans that the user has accepted
    accepted_plans = MovementPlan.objects.filter(
        ship_fac=dmm.fac
    ).filter(
        result=MovementPlan.Result.accepted
    )

    # our list of lists
    list_of_plans = []
    # column headers
    column_headers = [
        'Sending Facility', 
        'Receiving Facility', 
        'Date Requested', 
        'Expense Account Desc', 
        'Expense Account No', 
        'Item Description', 
        'Item IMMS No', 
        'Item Mfr Cat No', 
        'Shipping Qty', 
        'LUOM Cost',
        'EXT Cost',
    ]
    list_of_plans.append(column_headers)

    # iterate through the query set and append desired fields to new list
    for plan in accepted_plans:
        plan_x = []

        ext = plan.accepted_qty * plan.item.luom_cost
        
        plan_x.append(plan.item.fac)
        plan_x.append(plan.ship_fac)
        plan_x.append(plan.created_at)
        plan_x.append(plan.item.expense_account_desc)
        plan_x.append(plan.item.expense_account_no)
        plan_x.append(plan.item.description)
        plan_x.append(plan.item.imms)
        plan_x.append(plan.item.mfr_cat_no)
        plan_x.append(plan.accepted_qty)
        plan_x.append(plan.item.luom_cost)
        plan_x.append(ext)

        list_of_plans.append(plan_x)

    return ExcelResponse(list_of_plans, output_filename=f'Reduction App Accepted Items {t_month} {t_day} {t_year}')
    
@login_required
def completed_export_excel(request):
    # facility of requesting dmm
    dmm = Facility.objects.filter(dmm=request.user)[0]

    # get the date for the output filename
    t_day = dt.datetime.today().day
    t_month = dt.datetime.today().month
    t_year = dt.datetime.today().year

    # queryset of plans that the user has accepted
    completed_plans = MovementPlan.objects.filter(
        dmm=request.user
    ).filter(
        result=MovementPlan.Result.accepted
    )

    # our list of lists
    list_of_plans = []
    # column headers
    column_headers = [
        'Sending Facility', 
        'Receiving Facility', 
        'Date Requested', 
        'Expense Account Desc', 
        'Expense Account No', 
        'Item Description', 
        'Item IMMS No', 
        'Item Mfr Cat No', 
        'Shipping Qty', 
        'LUOM Cost',
        'EXT Cost'
        'Reduction Method',
    ]
    list_of_plans.append(column_headers)

    # iterate through the query set and append desired fields to new list
    for plan in completed_plans:
        plan_x = []

        ext = plan.item.luom_cost * plan.accepted_qty
        
        plan_x.append(plan.item.fac)
        plan_x.append(plan.ship_fac)
        plan_x.append(plan.created_at)
        plan_x.append(plan.item.expense_account_desc)
        plan_x.append(plan.item.expense_account_no)
        plan_x.append(plan.item.description)
        plan_x.append(plan.item.imms)
        plan_x.append(plan.item.mfr_cat_no)
        plan_x.append(plan.accepted_qty)
        plan_x.append(plan.item.luom_cost)
        plan_x.append(ext)
        plan_x.append(plan.decision)

        list_of_plans.append(plan_x)

    return ExcelResponse(list_of_plans, output_filename=f'Reduction App Reduced Items {t_month} {t_day} {t_year}')

@login_required
def view_requests(request):

    # get all outstanding plans for review
    outstanding_plans = MovementPlan.objects.filter(
        result=MovementPlan.Result.outstanding
    ).exclude(
        ship_fac='000'
    ).order_by(
        '-ship_fac'
    )

    context = {
        'outstanding_plans': outstanding_plans,
    }

    return render(request, 'act/review_requests.html', context)