from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse

import json

from .models import CountUsageList, MovementPlan
from .forms import MovementPlanForm
from inventory.models import Facility

@login_required
def count_usage_list(request):
    dmm = Facility.objects.filter(dmm=request.user)[0]

    context = {
        'no_move_list': CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            issue_qty=0
        ).filter(
            luom_po_qty=0
        ).filter(
            count_qty__gt=0
        ).filter(
            isTarget=False
        )[:100]
    }

    return render(request, 'target/target_list.html', context)

# View for reviewing target items and setting movement plans
@login_required
def review_target_items(request):
    dmm = Facility.objects.filter(dmm=request.user)[0]

    # get all plans for displaying result status
    all_plans = MovementPlan.objects.all()
    
    # get a list of item ids with movement plans that are outstanding
    plans_outstanding = MovementPlan.objects.filter(
        result=MovementPlan.Result.outstanding
    )
    outstanding_ids = []
    for i in plans_outstanding:
        outstanding_ids.append(i.item_id)

    # get a list of item ids with movement plans that are not outstanding
    plans_not_outstanding = MovementPlan.objects.exclude(
        result=MovementPlan.Result.outstanding
    )
    not_outstanding_ids = []
    for i in plans_not_outstanding:
        not_outstanding_ids.append(i.item_id)

    context = {
        'target_list': CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            issue_qty=0
        ).filter(
            luom_po_qty=0
        ).filter(
            count_qty__gt=0
        ).filter(
            isTarget=True
        )[:100],
        'outstanding_ids': outstanding_ids,
        'not_outstanding_ids': not_outstanding_ids,
        'all_plans': all_plans,
    }

    return render(request, 'target/review_targets.html', context)

@login_required
def move_targets(request, pk):
    d_facility = Facility.objects.filter(dmm=request.user)[0]
    item_from_id = get_object_or_404(CountUsageList, pk=pk)

    matched_items = CountUsageList.objects.filter(mfr_cat_no=item_from_id.mfr_cat_no)

    if request.method == 'POST':
        form = MovementPlanForm(request.POST)
        form.instance.dmm = request.user
        form.instance.item = item_from_id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('review-targets',))
    else:
        form = MovementPlanForm()

    context = {
        'target_item': item_from_id,
        'matched_items': matched_items,
        'd_facility': d_facility,
        'form': form,
    }

    return render(request, 'target/target_movement.html', context)

# Toggle true and false for isTarget on no move items
@login_required
@ensure_csrf_cookie
def target_item_true(request, pk):
    if request.method == 'POST':
        item_from_id = get_object_or_404(CountUsageList, pk=pk)
        bool_before = item_from_id.isTarget
        item_from_id.isTarget = True
        item_from_id.save(update_fields=['isTarget'])
        bool_after = item_from_id.isTarget

    response_data = {
        'django_response': f'item was isTarget of... {bool_before} and is now set to... {bool_after}'
    }

    return JsonResponse(response_data)

@login_required
@ensure_csrf_cookie
def target_item_false(request, pk):
    if request.method == 'POST':
        item_from_id = get_object_or_404(CountUsageList, pk=pk)
        bool_before = item_from_id.isTarget
        item_from_id.isTarget = False
        item_from_id.save(update_fields=['isTarget'])
        bool_after = item_from_id.isTarget

    response_data = {
        'django_response': f'item was isTarget of... {bool_before} and is now set to... {bool_after}'
    }

    return JsonResponse(response_data)
