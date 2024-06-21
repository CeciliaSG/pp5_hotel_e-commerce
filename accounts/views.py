from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from booking.models import SpaBooking
from .forms import CustomerProfileForm
from .models import CustomerProfile


@login_required
def profile(request):
    """

    From Boutique Ado walkthrough.
    
    Display and update the user's profile information.

    This view retrieves the CustomerProfile for the currently logged-in user.
    It handles both GET and POST requests:
    - For GET requests, it displays the profile form pre-filled with the user's information.
    - For POST requests, it updates the profile with the submitted data if the form is valid.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered profile page.

    Raises:
        Http404: If the CustomerProfile does not exist for the current user.

    Context:
        form (CustomerProfileForm): The form for displaying and updating the user's profile.
        spa_bookings (QuerySet): The set of SpaBooking objects associated with the user's profile.
        customer_name (str): The username of the current user.
        messages (Message): The messages to display to the user.
    """

    profile = get_object_or_404(CustomerProfile, user=request.user)
    #user = request.user

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

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
        'A confirmation email was sent on the booking date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'spa_bookings': spa_bookings,
    }

    return render(request, template, context)