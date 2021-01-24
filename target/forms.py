from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import MovementPlan, CountUsageList


class MovementPlanForm(forms.ModelForm):

    class Meta:
        model = MovementPlan
        fields = ['ship_qty', 'decision', 'ship_fac']
        labels = {
            'ship_qty': _('Quantity'),
            'ship_fac': _('Destination Facility'),
        }
        help_texts = {
            'ship_qty': _("how many units would you like to remove from your facility?"),
            'ship_fac': _("which facility would you like to send to? If not shipping, select not shipping"),
        }
        widgets = {
            'decision': forms.RadioSelect(),
        }