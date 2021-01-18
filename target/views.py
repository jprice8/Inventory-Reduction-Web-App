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
            po_qty=0
        ).filter(
            count_qty__gt=0
        ).filter(
            isTarget=False
        )[:100],
        'target_list': CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            issue_qty=0
        ).filter(
            po_qty=0
        ).filter(
            count_qty__gt=0
        ).filter(
            isTarget=True
        )[:100]
    }
    return render(request, 'target/target_list.html', context)

@login_required
def move_targets(request, pk):
    dmm = Facility.objects.filter(dmm=request.user)[0]
    item_from_id = get_object_or_404(CountUsageList, pk=pk)

    matched_items = CountUsageList.objects.filter(mfr_cat_no=item_from_id.mfr_cat_no)

    if request.method == 'POST':
        form = MovementPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('count-usage-list', args=(pk,)))
    else:
        form = MovementPlanForm()

    context = {
        'target_item': item_from_id,
        'matched_items': matched_items,
        'dmm': dmm,
        'form': form,
    }

    return render(request, 'target/target_movement.html', context)

# @login_required
# @ensure_csrf_cookie
# def ajax_post_target(request):
#     listing_from_item = json.loads(request.body)['listing_data']
#     id_from_item = json.loads(request.body)['item_id']

#     # get objects with that id
#     item_from_id = CountUsageList.objects.get(pk=id_from_item)
#     # print(f"old listing: {item_from_id.listing}")
#     item_from_id.listing = listing_from_item
#     item_from_id.save(update_fields=['listing'])

#     # print(f"new listing: {item_from_id.listing}")

#     # do something with the data from the POST request
#     # if sending data back to the view, create the data dictionary
#     data = {
#         'django_response': 'success',
#     }
#     return JsonResponse(data)

# @login_required
# @ensure_csrf_cookie
# def ajax_reduction_qty(request):
#     reduction_from_item = json.loads(request.body)['reduction_data']
#     id_from_item = json.loads(request.body)['item_id']

#     item_from_id = CountUsageList.objects.get(pk=id_from_item)
#     print(f"old reduction qty: {item_from_id.reduction_qty}")
#     item_from_id.reduction_qty = reduction_from_item
#     print(f"new reduction qty: {reduction_from_item}")
#     item_from_id.save(update_fields=['reduction_qty'])

#     response_data = {
#         'django_response': 'Successfully edited request quantity.',
#     }

#     return JsonResponse(response_data)

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
