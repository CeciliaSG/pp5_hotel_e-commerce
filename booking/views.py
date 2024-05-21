from django.shortcuts import render
from .forms import SpaBookingForm, SpaBookingServicesFormSet
from .models import SpaBooking, SpaBookingServices
from datetime import datetime
from django.shortcuts import redirect




# Create your views here.

def book_spa_service(request, context_only=False):
    if request.method == 'POST':
        booking_form = SpaBookingForm(request.POST)
        service_formset = SpaBookingServicesFormSet(request.POST)

        if booking_form.is_valid() and service_formset.is_valid():
            booking = booking_form.save(commit=False)

            booking.customer_profile = request.user
    
            
            booking.date_and_time = datetime.now()  
            booking.booking_date = datetime.now()  
            
            booking.booking_total = 0
            booking.save()

            for service_form in service_formset:
                service = service_form.save(commit=False)
                service.spa_booking = booking
                service.save()

            booking.update_total()

            return redirect('home')

    else:
        booking_form = SpaBookingForm()
        service_formset = SpaBookingServicesFormSet()

    context = {
        'booking_form': booking_form,
        'service_formset': service_formset,
    }
    if context_only:
        return context
    else:
        return render(request, 'booking/book_spa_service.html', context)