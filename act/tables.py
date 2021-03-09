from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.humanize.templatetags.humanize import naturalday
import django_tables2 as tables
from django_tables2.utils import Accessor
from target.models import CountUsageList, MovementPlan

from functools import reduce

class FloatColumn(tables.Column):
    def render(self, value):
        return '${:,.2f}'.format(value)

class IntColumn(tables.Column):
    def render(self, value):
        return '{:,.0f}'.format(value)

class DateColumn(tables.Column):
    def render(self, value):
        return value.strftime('%b %d %Y')


class CountUsageListReviewTable(tables.Table):
    period = DateColumn(verbose_name="Count Date")
    count_qty = IntColumn(verbose_name="Remaining Qty")
    issue_qty = IntColumn(verbose_name="Issue Qty")
    luom_po_qty = IntColumn(verbose_name="PO Qty")
    imms_create_date = DateColumn()
    uom_conv = IntColumn()
    luom_cost = FloatColumn(verbose_name="Ext Cost", orderable=False)
    shipped_qty = tables.Column(verbose_name="Shipped Qty")

    class Meta:
        model = CountUsageList
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'period', 
            'imms', 
            'count_qty', 
            'issue_qty', 
            'luom_po_qty',
            'mfr',
            'mfr_cat_no',
            'description',
            'imms_create_date',
            'expense_account_no',
            'default_uom',
            'uom_conv',
            'uom',
            'shipped_qty',
            'luom_cost',
        )

    def render_count_qty(self, value, record):
        def my_add(a, b):
            result = a + b
            return result
        
        if record.shipped_qty:
            return value - reduce(my_add, record.shipped_qty)
        else:
            return value

    def render_luom_cost(self, value, record):
        # function for reducing shipped qty
        def my_add(a, b):
            result = a + b 
            return result

        # get remaining qty
        if record.shipped_qty:
            remaining_qty = record.count_qty - reduce(my_add, record.shipped_qty)
        else:
            remaining_qty = record.count_qty

        # calc new ext cost
        new_ext_cost = value * remaining_qty
        return '${:,.2f}'.format(new_ext_cost)


#### Movement Plan Review Table ####
class MovementPlanReviewTable(tables.Table):
    item_fac = tables.Column(accessor='item.fac', verbose_name='Sending Facility')
    item_imms = tables.Column(accessor='item.imms')
    item_expense_acct_no = tables.Column(accessor='item.expense_account_no', verbose_name='Expense Account Number')
    item_description = tables.Column(accessor='item.description')
    item_mfr = tables.Column(accessor='item.mfr')
    item_mfr_cat_no = tables.Column(accessor='item.mfr_cat_no')
    item_luom_cost = FloatColumn(accessor='item.luom_cost', verbose_name='Accepted Ext Cost', orderable=False)

    dmm = tables.Column(verbose_name='Sending DMM')
    ship_fac = tables.Column(verbose_name='Destination')
    created_at = tables.Column(verbose_name='DateTime Requested')
    accepted_qty = tables.Column(verbose_name='Accepted Quantity')
    
    class Meta:
        model = MovementPlan
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'decision',
            'result',
        )
        sequence = (
            'dmm',
            'item_fac',
            'created_at',
            'decision',
            'ship_fac',
            'result',
            'accepted_qty',
            'item_imms',
            'item_description',
            'item_mfr',
            'item_mfr_cat_no',
            'item_expense_acct_no',
            'item_luom_cost',
        )

    def render_item_luom_cost(self, value, record):
        # multiply accepted qty by luom cost to get ext cost
        accepted_ext_cost = value * record.accepted_qty
        return '${:,.2f}'.format(accepted_ext_cost)