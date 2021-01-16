from django.db import models


class CountUsageList(models.Model):
    period = models.DateTimeField(null=False)
    fac = models.CharField(max_length=50, null=False)
    imms = models.CharField(max_length=50, null=False)
    count_qty = models.IntegerField(null=False)
    issue_qty = models.IntegerField(null=False)
    po_qty = models.IntegerField(null=False)
    facility_name = models.CharField(max_length=50, null=False)
    mfr = models.CharField(max_length=100, null=False)
    mfr_cat_no = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    imms_create_date = models.DateTimeField(null=False)
    vendor = models.CharField(max_length=100, null=False)
    vend_cat_no = models.CharField(max_length=100, null=False)
    default_uom = models.CharField(max_length=10, null=False)
    default_uom_conv = models.IntegerField(null=False)
    default_uom_price = models.FloatField(null=False)
    luom = models.CharField(max_length=10, null=False)
    luom_conv = models.IntegerField(null=False)
    ext_cost = models.FloatField(null=False)
    reduction_qty = models.IntegerField(null=False, default=0)
    LISTINGS = (
        (1, 'No Move'),
        (2, 'Target'),
        (3, 'Completed'),
    )
    listing = models.IntegerField(null=False, default=1, choices=LISTINGS)

    class Meta:
        ordering = ('-ext_cost', )

    def __str__(self):
        return f'item: {self.description}, at facility: {self.fac}, with qty: {self.count_qty}'

    def is_no_move(self):
        # if issue_qty and po_qty are false then yes.
        if self.issue_qty == 0 & self.po_qty == 0:
            return True
