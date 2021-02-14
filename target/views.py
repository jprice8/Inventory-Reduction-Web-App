from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Sum, Count

import json, os

from .models import CountUsageList, MovementPlan, TenetPO
from .forms import MovementPlanForm
from inventory.models import Facility

from reductionapp.settings import EMAIL_HOST_USER

@login_required
def no_intake_list(request):
    debug = os.environ.get("DJANGO_DEBUG", False)
    matching_facility = Facility.objects.filter(dmm=request.user)

    if matching_facility.exists():
        dmm = Facility.objects.filter(dmm=request.user)[0]
    else:
        return render(request, 'inventory/non_dmm_redir.html')


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
        )[:100],
        'DEBUG': debug,
    }

    return render(request, 'target/no_intake_list.html', context)

# View for reviewing target items and setting movement plans
@login_required
def review_target_items(request):
    debug = os.environ.get("DJANGO_DEBUG", False)
    dmm = Facility.objects.filter(dmm=request.user)[0]

    # get all plans for displaying result status
    all_plans = MovementPlan.objects.all()

    # get total number of plans set for an item
    agg_plans_per_item = all_plans.values(
        'item'
    ).annotate(
        agg_plans=Count('id')
    )
    
    # get all item ids from plans
    plan_ids = []
    for i in all_plans:
        plan_ids.append(i.item_id)

    target_items_list = CountUsageList.objects.filter(
        fac=dmm.fac
    ).filter(
        count_qty__gt=0
    ).filter(
        isTarget=True
    ).filter(
        isHidden=False
    )[:100]

    context = {
        'target_list': target_items_list,
        'DEBUG': debug,
        'agg_plans': agg_plans_per_item,
        'plan_ids': plan_ids,
    }

    return render(request, 'target/review_targets.html', context)

#### Set Movement Plan Form ####

@login_required
def move_targets(request, pk):
    d_facility = Facility.objects.filter(dmm=request.user)[0]
    item_from_id = get_object_or_404(CountUsageList, pk=pk)

    # Get matching count usage items from within system that match the mfr_cat_no
    matched_items = CountUsageList.objects.filter(
        mfr_cat_no=item_from_id.mfr_cat_no
    ).order_by(
        '-issue_qty'
    )

    # Get matching tenet pos from all of Tenet that match the mfr cat no
    matched_pos = TenetPO.objects.filter(
        mfr_cat_no=item_from_id.mfr_cat_no
    ).exclude(
       market='SAN ANTONIO' 
    ).order_by(
        '-luom_qty'
    )

    if request.method == 'POST':
        form = MovementPlanForm(request.POST)
        form.instance.dmm = request.user
        form.instance.item = item_from_id
        if form.is_valid():
            # error handle trying to submit higher qty
            request_qty = form.cleaned_data['ship_qty']
            available_qty = item_from_id.count_qty
            if request_qty > available_qty:
                return HttpResponse(f"<h2>You are trying to reduce {request_qty} units which is more than your recorded inventory quantity of {available_qty}. Please go back and try again.</h2>")
            else:

                # Send email notification to receiving dmm
                # subject = 'You have received a movement request on The Reduction App'
                # receiving_dmm = request.POST['ship_fac']
                # message = f'Facility {receiving_dmm}, you have received a movement request from DMM: {request.user}. Please go to reductiontoolkit.com to handle the request.'
                # email_from = EMAIL_HOST_USER
                # recipient_list = [request.user.email,]
                # send_mail(subject, message, email_from, recipient_list)

                form.save()
                return HttpResponseRedirect(reverse('review-targets',))
        else:
            print(form.errors)
    else:
        form = MovementPlanForm(initial={'item_id': pk})

    context = {
        'target_item': item_from_id,
        'matched_items': matched_items,
        'matched_pos': matched_pos,
        'd_facility': d_facility,
        'form': form,
    }

    return render(request, 'target/target_movement.html', context)

#### API views ####

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

@login_required
@ensure_csrf_cookie
def hide_target(request, pk):
    if request.method == 'POST':
        item_from_id = get_object_or_404(CountUsageList, pk=pk)
        item_from_id.isHidden = True
        item_from_id.save(update_fields=['isHidden'])

    response_data = {
        'django_response': f'item {item_from_id} is now hidden'
    }

    return JsonResponse(response_data)

# See all plans for a given item. Triggered from review target items page.
@login_required
def see_item_plans(request, pk):
    # get item from id
    item_from_id = CountUsageList.objects.get(pk=pk)
    # get all plans for the id
    plans_for_item = MovementPlan.objects.filter(
        item=item_from_id
    )

    context = {
        'plans_for_item': plans_for_item,
        'item_from_id': item_from_id,
    }

    return render(request, 'target/see_item_plans.html', context)
