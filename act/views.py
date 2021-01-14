from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def act_page(request):
    return render(request, 'act/act_page.html')