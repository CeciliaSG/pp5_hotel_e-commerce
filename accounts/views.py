from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile

# Create your views here.

@login_required
def customer_profile(request):
    profile = get_object_or_404(CustomerProfile, customer=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/customer_profile.html', context)
