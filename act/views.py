from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from inventory.models import Facility

@login_required
def act_page(request):
    context = {
        'facility': Facility.objects.filter(dmm=request.user)[0]
    }

    return render(request, 'act/act_page.html', context)