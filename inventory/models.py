from django.db import models
from django.contrib.auth.models import User


class Invcount(models.Model):
    period = models.DateTimeField(null=False)
    fac = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=50)
    unit_id = models.CharField(max_length=100, null=True)
    imms = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=255, null=True)
    vendor = models.CharField(max_length=100, null=True)
    mfr_cat_no = models.CharField(max_length=50, null=True)
    qty = models.IntegerField(default=0, null=False)
    cost = models.FloatField(default=0, null=False)
    uom = models.CharField(max_length=50, null=True)
    ext = models.FloatField(default=0, null=False)

    class Meta:
        ordering = ('-ext', )

    def __str__(self):
        return f'item: {self.description}, at facility: {self.fac}, with qty: {self.qty} and ext: {self.ext}'


class Facility(models.Model):
    fac = models.CharField(null=False, max_length=50)
    facility_name = models.CharField(null=False, max_length=100, default='939')
    dmm = models.ForeignKey(User, null=False, on_delete=models.CASCADE)