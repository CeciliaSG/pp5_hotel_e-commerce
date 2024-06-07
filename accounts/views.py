from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile
from booking.models import SpaBooking
from .forms import CustomerProfileForm
from django.contrib import messages


@login_required
def profile(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    user = request.user

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            user.email = profile.default_email
            user.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('customer_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)
    else:
        form = CustomerProfileForm(instance=profile)

    spa_bookings = SpaBooking.objects.filter(customer_profile=profile)
    username = request.user.username

    context = {
        'form': form,
        'spa_bookings': spa_bookings,
        'customer_name': profile.user.username,
        'messages': messages.get_messages(request),
    }
    return render(request, 'accounts/customer_profile.html', context)



def booking_history(request, booking_number):
    booking = get_object_or_404(SpaBooking, booking_number=booking_number)
    spa_bookings = SpaBooking.objects.all()

    messages.info(request, (
        f'This is a past confirmation for booking number {booking_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'spa_bookings': spa_bookings,
        #'from_profile': True,
    }

    return render(request, template, context)