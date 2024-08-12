from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect

from allauth.account.views import ConfirmEmailView
from django.http import HttpResponseRedirect
from django.urls import reverse

from booking.models import SpaBooking
from .forms import UserProfileForm, CustomerProfileForm
from django.urls import reverse
from allauth.account.views import LoginView
from .models import CustomerProfile
from .forms import DeleteAccountForm


@login_required
def profile(request):
    """

    From Boutique Ado walkthrough.

    Display and update the user's profile information.

    This view retrieves the CustomerProfile for the
    currently logged-in user.
    It handles both GET and POST requests:
    - For GET requests, it displays the profile form pre-filled
    with the user's information.
    - For POST requests, it updates the profile with the submitted
    data if the form is valid.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the
        rendered profile page.

    Raises:
        Http404: If the CustomerProfile does not exist for
        the current user.

    Context:
        form (CustomerProfileForm): The form for displaying and
        updating the user's profile.
        spa_bookings (QuerySet): The set of SpaBooking objects
        associated with the user's profile.
        customer_name (str): The username of the current user.
        messages (Message): The messages to display to the user.
    """

    try:
        user = request.user 
        profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        messages.warning(request, "No profile found for this user.")
        return redirect('signup.html')

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = CustomerProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile.email = user.email
            profile_form.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('customer_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = CustomerProfileForm(instance=profile)

    spa_bookings = SpaBooking.objects.filter(customer_profile=profile)
    username = request.user.username

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_email': user.email,
        'spa_bookings': spa_bookings,
        'customer_name': profile.user.username,
        'messages': messages.get_messages(request),
    }
    return render(request, 'accounts/customer_profile.html', context)


class CustomConfirmEmailView(ConfirmEmailView):

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        if self.object and self.object.email_address.verified:
            return HttpResponseRedirect(reverse('account_login'))
        return response

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self.object and self.object.email_address.verified:
            return HttpResponseRedirect(reverse('account_login'))
        return response
        

def booking_history(request, booking_number):
    """
    Display the booking history and details of a
    specific SpaBooking identified by its booking number.

    This view retrieves a specific SpaBooking object using
    the provided booking_number. If the booking
    exists, it renders a template ('checkout/checkout_success.html')
    with details of the booking and
    a list of all SpaBooking objects for reference.

    Parameters:
    - request: HttpRequest object representing the request made
    by the user.
    - booking_number: str, the unique booking number of
    the SpaBooking to display.

    Raises:
    - Http404: If no SpaBooking object exists with the
    provided booking_number.

    Returns:
    - HttpResponse: Renders 'checkout/checkout_success.html'
    template with the following context:
      {
          'booking': SpaBooking object with the specified booking_number,
          'spa_bookings': QuerySet of all SpaBooking objects,
      }
    """
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


@login_required
def delete_profile(request):
    """
    Handle the deletion of the user's profile and related data.

    This view allows a user to delete their profile and associated data.
    It will delete the associated CustomerProfile, any SpaBookings related
    to the profile, and finally the user account itself. It also handles
    user logout and displays appropriate messages.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered template or redirect.
    """
    profile = get_object_or_404(CustomerProfile, user=request.user)

    try:
        profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        return redirect('customer_profile')

    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm_delete']:
            try:
                SpaBooking.objects.filter(customer_profile=profile).delete()
                profile.delete()
                request.user.delete()
                logout(request)

                messages.success(request, 'Your profile and related data have been deleted.')
                return redirect('home') 
            except Exception as e:
                messages.error(request, f'Failed to delete profile: {str(e)}')
                return redirect('delete_profile')
    else:
        form = DeleteAccountForm()

    return render(request, 'accounts/delete_profile.html', {'form': form})