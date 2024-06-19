from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .forms import ServiceBookingForm, TimeSlotSelectionForm
from services.models import SpaService, Availability, TimeSlot


#from django.forms.widgets import DateInput

def book_spa_service(request):
    form = ServiceBookingForm()
    time_slot_form = TimeSlotSelectionForm()
    selected_service = None
    selected_date = None
    quantity = None
    available_time_slots = []
    price = None
    is_access = None

    if request.method == "POST":
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            selected_service = form.cleaned_data.get("spa_service")
            selected_date = form.cleaned_data.get("date")
            quantity = form.cleaned_data.get("quantity")
            selected_service_id = request.POST.get('service')
            selected_service = get_object_or_404(SpaService, pk=selected_service_id)

            if selected_service:
                price = selected_service.price
                is_access = selected_service.is_access 

            if selected_service and selected_date:
                available_time_slots = TimeSlot.objects.filter(availability__spa_service=selected_service, availability__specific_dates__date=selected_date)

    return render(
        request,
        "booking/book_spa_service.html",
        {
            "form": form,
            "time_slot_form": time_slot_form,
            "service_id": selected_service.id if selected_service else None,
            "selected_date": selected_date,
            "quantity": quantity,
            "available_time_slots": available_time_slots,
            "price": price,
            "is_access": is_access,
        },
    )