import django_tables2 as tables
from target.models import CountUsageList


class NoIntakeReviewTable(tables.Table):
    class Meta:
        model = CountUsageList
        template_name = 'act/review_no_intake.html'
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
            'ext_cost'
        )