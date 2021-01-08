from django.db import models
from django.contrib.auth.models import User


class Invcount(models.Model):
    period = models.DateTimeField()
    fac = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    unit_id = models.CharField(max_length=100, null=True)
    imms = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)
    vendor = models.CharField(max_length=100, null=True)
    mfr_cat_no = models.CharField(max_length=50, null=True)
    qty = models.IntegerField(default=0)
    cost = models.FloatField(null=True)
    uom = models.CharField(max_length=50, null=True)
    ext = models.FloatField(null=True)

    class Meta:
        ordering = ('-ext', )

    def __str__(self):
        return f'item: {self.description}, at facility: {self.fac}, with qty: {self.qty} and ext: {self.ext}'
