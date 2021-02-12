from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CountUsageList(models.Model):
    fac = models.CharField(max_length=50, null=False)
    period = models.DateTimeField(null=False)
    imms = models.CharField(max_length=50, null=False)
    uom = models.CharField(max_length=10, null=False)
    count_qty = models.IntegerField(null=False)
    issue_qty = models.IntegerField(null=False)
    luom_po_qty = models.IntegerField(null=False)
    facility_name = models.CharField(max_length=50, null=False)
    mfr = models.CharField(max_length=100, null=False)
    mfr_cat_no = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    imms_create_date = models.DateTimeField(null=False)
    vendor = models.CharField(max_length=100, null=False)
    vend_cat_no = models.CharField(max_length=100, null=False)
    uom_conv = models.IntegerField(null=False)
    uom_price = models.FloatField(null=False)
    default_uom = models.CharField(max_length=10, null=False)
    luom_no_of_units = models.IntegerField(null=False)
    luom_cost = models.FloatField(null=False)
    expense_account_no = models.CharField(max_length=100, null=False, default="null")
    expense_account_desc = models.CharField(max_length=100, null=False, default="null")
    ext_cost = models.FloatField(null=False)
    reduction_qty = models.IntegerField(null=False, default=0)
    isTarget = models.BooleanField(null=False, default=False)

    class Meta:
        ordering = ('-ext_cost', )

    def __str__(self):
        return f'item: {self.description}, at facility: {self.fac}, with qty: {self.count_qty}'

    def is_no_move(self):
        # if issue_qty and po_qty are false then yes.
        if self.issue_qty == 0 & self.po_qty == 0:
            return True


class MovementPlan(models.Model):
    dmm = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(CountUsageList, on_delete=models.CASCADE)
    ship_qty = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_qty = models.IntegerField(null=False, default=0)

    class MovementOptions(models.TextChoices):
        system = 'system', _('Ship to a facility within the system'),
        tenet = 'tenet', _('Ship to a facility outside of the system'),
        sell = 'sell', _('Sell to a third party vendor'),
        discard = 'discard', _('Discard the item'),

    decision = models.CharField(
        max_length=50, 
        choices=MovementOptions.choices,
        default=MovementOptions.system,
    )

    class ShipFacilities(models.TextChoices):
        TEN = 'TEN', _('Shipping to Tenet Facility')
        DIS = 'DIS', _('Selling or Discarding')
        BMC = '939', _('Baptist Medical Center')
        MTB = '971', _('Mission Trail Baptist Hospital')
        SLB = '952', _('Saint Lukes Baptist Hospital')
        RHH = '872', _('Resolute Health Hospital')
        NBH = '968', _('Northeast Baptist Hospital')
        NCB = '954', _('North Central Baptist Hospital')

    ship_fac = models.CharField(
        max_length=3,
        choices=ShipFacilities.choices,
    )
    
    class Result(models.TextChoices):
        outstanding = 'outstanding', _('Outstanding')
        accepted = 'accepted', _('Accepted')
        rejected = 'rejected', _('Rejected')
        sold = 'sold', _('Sold')
        discarded = 'discarded', _('Discarded')

    result = models.CharField(
        max_length=50,
        choices=Result.choices,
        default=Result.outstanding,
    )

    def __str__(self):
        return f'movement plan by {self.dmm}, to facility: {self.ship_fac}, for item: {self.item.mfr_cat_no}, created on {self.created_at}, status: {self.result}'

    def calc_accepted_ext(self):
        # multiply accepted qty by the items luom cost.
        return self.accepted_qty * self.item.luom_cost

    def calc_proposed_ext(self):
        # multiply ship qty by the items luom cost.
        return self.ship_qty * self.item.luom_cost


class TenetPO(models.Model):
    group = models.CharField(max_length=100, null=False)
    market = models.CharField(max_length=100, null=False)
    facility_name = models.CharField(max_length=100, null=False)
    fac = models.CharField(max_length=100, null=False)
    imms = models.CharField(max_length=50, null=False)
    mfr_cat_no = models.CharField(max_length=100, null=False)
    luom = models.CharField(max_length=50, null=False)
    luom_qty = models.IntegerField(null=False)

    def __str__(self):
        return f'po from {self.facility_name}, for cat no: {self.mfr_cat_no}, qty: {self.luom_qty}'