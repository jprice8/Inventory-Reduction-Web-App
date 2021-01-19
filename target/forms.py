from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import MovementPlan


class MovementPlanForm(forms.ModelForm):
    class Meta:
        model = MovementPlan
        fields = ['ship_qty', 'isMove', 'isSell', 'isTrash', 'ship_fac']
        labels = {
            'ship_qty': _('Quantity'),
            'isMove': _('Move'),
            'isSell': _('Sell'),
            'isTrash': _('Discard'),
            'ship_fac': _('Destination Facility'),
        }
        help_texts = {
            'ship_qty': _("how many units would you like to remove from your facility?"),
            'isMove': _("select to move units to another facility within the health system"),
            'isSell': _("select to sell units to a third party vendor"),
            'isTrash': _("select if not able to move or sell. Indicates you are writing item off and discarding"),
            'ship_fac': _("which facility would you like to send to? If not moving, select not shipping"),
        }