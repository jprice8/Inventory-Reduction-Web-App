from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.humanize.templatetags.humanize import naturalday
import django_tables2 as tables
from target.models import CountUsageList, MovementPlan

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
    count_qty = IntColumn()
    issue_qty = IntColumn()
    luom_po_qty = IntColumn(verbose_name="PO Qty")
    imms_create_date = DateColumn()
    uom_conv = IntColumn()
    luom_cost = FloatColumn()
    ext_cost = FloatColumn()

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
            'luom_cost',
            'ext_cost',
        )


#### Movement Plan Review Table ####
class MovementPlanReviewTable(tables.Table):
    item_fac = tables.Column(accessor='item.fac', verbose_name='Sending Facility')
    item_imms = tables.Column(accessor='item.imms')
    item_expense_acct_no = tables.Column(accessor='item.expense_account_no', verbose_name='Expense Account Number')
    item_description = tables.Column(accessor='item.description')
    item_mfr = tables.Column(accessor='item.mfr')
    item_mfr_cat_no = tables.Column(accessor='item.mfr_cat_no')
    item_luom_cost = FloatColumn(accessor='item.luom_cost')

    dmm = tables.Column(verbose_name='Sending DMM')
    ship_fac = tables.Column(verbose_name='Destination')
    created_at = tables.Column(verbose_name='DateTime Requested')
    accepted_qty = tables.Column(verbose_name='Accepted Quantity')
    calc_accepted_ext = FloatColumn(verbose_name='Accepted Ext Cost')
    
    class Meta:
        model = MovementPlan
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'decision',
            'result',
            'calc_accepted_ext'
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
            'calc_accepted_ext',
        )