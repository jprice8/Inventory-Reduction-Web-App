from django import forms
from .models import MovementPlan


class MovementPlanForm(forms.ModelForm):
    class Meta:
        model = MovementPlan
        fields = ['ship_qty', 'isMove', 'isSell', 'isTrash', 'ship_fac']