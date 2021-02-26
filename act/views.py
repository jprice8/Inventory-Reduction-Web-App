from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from inventory.models import Facility
from target.models import CountUsageList, MovementPlan
from .tables import CountUsageListReviewTable, MovementPlanReviewTable

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
    )
    # get ext for no intake items
    no_intake_ext = 0
    for t in total_no_move:
        no_intake_ext += t.count_qty * t.luom_cost

    # total ext cost of items with intake at dmm's facility
    total_intake = CountUsageList.objects.filter(
        fac=dmm.fac
    ).filter(
        isTarget=False
    ).exclude(
        issue_qty=0, luom_po_qty=0
    )[:100]
    # get ext for intake items
    intake_ext = 0
    for t in total_intake:
        intake_ext += t.count_qty * t.luom_cost

    # total ext cost of targeted items
    total_target = CountUsageList.objects.filter(
        fac=dmm.fac
    ).filter(
        isTarget=True
    ).filter(
        isHidden=False
    )
    # get ext for items targeted
    targeted_ext = 0
    for t in total_target:
        targeted_ext +=  t.count_qty * t.luom_cost

    # total movement plan ext for action of not 0
    completed_plans = MovementPlan.objects.filter(
        dmm=request.user
    ).filter(
        isFinalized=True
    )

    # get completed ext for items reduced
    completed_ext = 0
    for plan in completed_plans:
        completed_ext += plan.accepted_qty * plan.item.luom_cost

    # get all plans dmm has accepted
    accepted_plans = MovementPlan.objects.filter(
        ship_fac=dmm.fac
    ).filter(
        isFinalized=True
    )

    # get accepted ext for items moving to dmm facility
    accepted_ext = 0
    for plan in accepted_plans:
        accepted_ext += plan.accepted_qty * plan.item.luom_cost

    # all movement plans with the user's facility listed as desired destination
    incoming_plans = MovementPlan.objects.filter(
        ship_fac=dmm.fac
    ).filter(
        result=MovementPlan.Result.outstanding
    ).order_by(
        'created_at', 'ship_fac' 
    )

    # all movement plans with the user listed as the requesting DMM
    outgoing_plans = MovementPlan.objects.filter(
        dmm=request.user
    ).exclude(
        isFinalized=True
    ).order_by(
        '-item', '-ship_qty'
    )

    context = {
        'facility': dmm,
        'no_move_ext': no_intake_ext,
        'intake_ext': intake_ext,
        'target_ext': targeted_ext,
        'completed_ext': completed_ext,
        'accepted_ext': accepted_ext,
        'incoming_plans': incoming_plans,
        'outgoing_plans': outgoing_plans,
        'DEBUG': debug,
    }

    return render(request, 'act/act_page.html', context)

#### API Views ####

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

# Dmm has completed the reduction and is ready to finalize the movement plan
@login_required
@ensure_csrf_cookie
def finalize_plan_handler(request, pk):
    # When finalize is pressed we need to:
    # 1. Make sure that status is not outstanding for all non-system.
    # 2. Update accepted qty to match ship qty for all non-system.
    # 3. Decrement accepted qty from inventory qty.
    # 4. Recalculate ext cost for the item.
    # 4. Flip isFinalized boolean.

    # get the plan
    plan = get_object_or_404(MovementPlan, pk=pk)

    # bifurcate into system vs non-system
    if request.method == 'POST':
        if plan.decision == MovementPlan.MovementOptions.system:
            # check the result. If accepted, win. If rejected, delete. Else, pass.
            if plan.result == MovementPlan.Result.accepted:
                # update count qty
                new_qty = plan.item.count_qty - plan.accepted_qty
                plan.item.count_qty = new_qty
                plan.item.save(update_fields=['count_qty'])

                # set isFinalized to True
                plan.isFinalized = True
                plan.save(update_fields=['isFinalized'])

            elif plan.result == MovementPlan.Result.rejected:
                # delete
                plan.delete()
            else:
                pass
        else:
            # for non-system:
            # change status to accepted.
            plan.result = MovementPlan.Result.accepted
            # update accepted qty from ship qty
            plan.accepted_qty = plan.ship_qty
            # set isFinalized to True
            plan.isFinalized = True
            plan.save(update_fields=['result', 'accepted_qty', 'isFinalized'])

            # update count qty
            new_qty = plan.item.count_qty - plan.accepted_qty
            plan.item.count_qty = new_qty
            plan.item.save(update_fields=['count_qty'])
            
    response_data = {
        'django_response': f'plan had isFinalized of...'
    }

    return JsonResponse(response_data)

#### Metric Views ####

# Top 100 Items With No Intake
class ItemsWithNoIntakeTableView(ExportMixin, SingleTableView):
    model = CountUsageList
    table_class = CountUsageListReviewTable
    template_name = 'act/review_no_intake.html'
    export_name = 'no_intake_items_list'

    def get_table_data(self, **kwargs):
        # get dmm variable
        dmm = Facility.objects.filter(dmm=self.request.user)[0]
        # get queryset for no intake items
        sliced_qs_ids = CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            issue_qty=0
        ).filter(
            luom_po_qty=0
        ).filter(
            isTarget=False
        ).values_list(
            'id', flat=True
        )[:100]

        no_intake_items = CountUsageList.objects.filter(id__in=sliced_qs_ids)

        return no_intake_items


# Top 100 Items With Intake
class ItemsWithIntakeTableView(ExportMixin, SingleTableView):
    model = CountUsageList
    table_class = CountUsageListReviewTable
    template_name = 'act/review_intake.html'
    export_name = 'intake_items_list'

    def get_table_data(self, **kwargs):
        # get dmm variable
        dmm = Facility.objects.filter(dmm=self.request.user)[0]
        # get queryset for intake items
        sliced_qs_ids = CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            isTarget=False
        ).exclude(
            issue_qty=0, luom_po_qty=0
        ).values_list(
            'id', flat=True
        )[:100]

        intake_items = CountUsageList.objects.filter(id__in=sliced_qs_ids)

        return intake_items

# Currently Targeted
class ReviewTargetedItemsTableView(ExportMixin, SingleTableView):
    model = CountUsageList
    table_class = CountUsageListReviewTable
    template_name = 'act/review_targeted.html'
    export_name = 'targeted_items_list'

    def get_table_data(self, **kwargs):
        # get dmm variable
        dmm = Facility.objects.filter(dmm=self.request.user)[0]
        # get queryset for targeted items
        targeted_items = CountUsageList.objects.filter(
            fac=dmm.fac
        ).filter(
            isTarget=True
        ).filter(
            isHidden=False
        )
        return targeted_items

# Removed Inventory
class ReviewCompletedPlansTableView(ExportMixin, SingleTableView):
    model = MovementPlan
    table_class = MovementPlanReviewTable
    template_name = 'act/review_completed.html'
    export_name = 'items_removed_from_facility'

    def get_table_data(self, **kwargs):
        # get queryset for removed items
        completed_plans = MovementPlan.objects.filter(
            dmm=self.request.user
        ).filter(
            isFinalized=True
        )
        return completed_plans

# Accepted Inventory
class ReviewAcceptedPlansTableView(ExportMixin, SingleTableView):
    model = MovementPlan
    table_class = MovementPlanReviewTable
    template_name = 'act/review_accepted.html'
    export_name = 'items_accepted_into_facility'

    def get_table_data(self, **kwargs):
        dmm = Facility.objects.filter(dmm=self.request.user)[0]
        # get queryset for removed items
        accepted_plans = MovementPlan.objects.filter(
            ship_fac=dmm.fac
        ).filter(
            isFinalized=True
        )
        return accepted_plans

#### Generic CBV's ####

class MovementPlanUpdate(UpdateView):
    model = MovementPlan
    fields = ['ship_qty']
    template_name = 'act/edit_plan_form.html'

    def get_success_url(self):
        return reverse('act-page')


class MovementPlanDelete(DeleteView):
    model = MovementPlan
    success_url = reverse_lazy('act-page')
    template_name = 'act/movementplan_confirm_delete.html'