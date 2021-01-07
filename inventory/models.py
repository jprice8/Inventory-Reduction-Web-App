from django.db import models
from django.contrib.auth.models import User


class Invcount(models.Model):
    period = models.DateTimeField()
    facility_no = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    unit_id = models.CharField(max_length=100)
    imms = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    vendor = models.CharField(max_length=100)
    mfr_cat_no = models.CharField(max_length=50)
    qty = models.IntegerField(default=0)
    cost = models.FloatField()
    uom = models.CharField(max_length=50)
    ext = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-ext', )

    def __str__(self):
        return f'item: {self.description} with qty: {self.qty} and ext: {self.ext}'

    def calculate_ext_cost(self):
        return self.qty * self.cost


class Issue(models.Model):
    facility_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    facility_no = models.CharField(max_length=50)
    dept_id = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    trans_code = models.CharField(max_length=100)
    issue_date = models.DateTimeField()
    imms = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    adjustment_number = models.CharField(max_length=100)
    qty = models.IntegerField(default=0)
    uom = models.CharField(max_length=50)
    wt_avg_cost = models.FloatField()
    ext_cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-ext_cost', )

    def __str__(self):
        return f'issue no: {self.adjustment_number}, facility no: {self.facility_no}, item name: {self.description}, ext: {self.ext_cost}'


class PurchaseOrder(models.Model): 
    facility_no = models.CharField(max_length=50)
    facility_name = models.CharField(max_length=100)
    po_date = models.DateTimeField()
    po_no = models.CharField(max_length=100)
    po_code = models.CharField(max_length=100)
    po_submit_type = models.CharField(max_length=100)
    vend_submit_type = models.CharField(max_length=100)
    po_line_no = models.IntegerField()
    imms = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    imms_vend_no = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    vendor_cat = models.CharField(max_length=100)
    imms_contr_exp = models.CharField(max_length=100)
    imms_contr_no = models.CharField(max_length=100)
    mfr = models.CharField(max_length=100)
    mfr_cat = models.CharField(max_length=100)
    expense_acct_no = models.CharField(max_length=100)
    expense_acct_desc = models.CharField(max_length=100)
    dept_acct_no = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    po_qty = models.IntegerField(default=0)
    po_price = models.FloatField()
    po_ext = models.FloatField()
    po_uom = models.CharField(max_length=100)
    po_uom_mult = models.IntegerField()
    low_uom_price = models.FloatField()

    class Meta:
        ordering = ('-po_ext', )

    def __str__(self):
        return f'purchase no: {self.adjustment_number}, facility no: {self.facility_no}, item name: {self.description}, ext: {self.po_ext}'
