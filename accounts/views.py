from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from booking.models import SpaBooking
from .forms import CustomerProfileForm
from .models import CustomerProfile


@login_required
def profile(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    #user = request.user

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            #if 'default_email' in form.cleaned_data:
                #user.email = form.cleaned_data['default_email']
                #user.save()

            #user.email = profile.default_email
            #user.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('customer_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)
    else:
        form = CustomerProfileForm(instance=profile)

    spa_bookings = SpaBooking.objects.filter(customer_profile=profile)
    username = request.user.username
    #customer_name = profile.user.get_full_name() or profile.user.username

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
        'A confirmation email was sent on the booking date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'spa_bookings': spa_bookings,
        #'from_profile': True,
    }

    return render(request, template, context)