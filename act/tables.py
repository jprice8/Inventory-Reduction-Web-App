from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.humanize.templatetags.humanize import naturalday
import django_tables2 as tables
from target.models import CountUsageList

class FloatColumn(tables.Column):
    def render(self, value):
        return '${:,.2f}'.format(value)

class IntColumn(tables.Column):
    def render(self, value):
        return '{:,.0f}'.format(value)

class DateColumn(tables.Column):
    def render(self, value):
        return value.strftime('%b %d %Y')

class NoIntakeReviewTable(tables.Table):
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