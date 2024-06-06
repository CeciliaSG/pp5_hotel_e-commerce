from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile
from booking.models import SpaBooking
from .forms import CustomerProfileForm
from django.contrib import messages


# Create your views here.

@login_required
def profile(request):
    profile = get_object_or_404(CustomerProfile, customer=request.user)
    #user = request.user

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            #user = request.user
            #user.email = profile.default_email
            #user.phone_number = profile.default_phone_number

            #messages.success(request, 'Profile updated successfully')
            return redirect('customer_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)  

    else:
        form = CustomerProfileForm(instance=profile)

    bookings = SpaBooking.objects.filter(customer_profile=profile)
    username = request.user.username
    form = CustomerProfileForm(instance=profile)

    context = {
        'form': form,
        'bookings': bookings,
        'customer_name': profile.customer.username,
    }
    return render(request, 'accounts/customer_profile.html', context)


def booking_history(request, booking_number):
    booking = get_object_or_404(SpaBooking, booking_number=booking_number)

    messages.info(request, (
        f'This is a past confirmation for order number {booking_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'from_profile': True,
    }

    return render(request, template, context)