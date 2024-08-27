from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .forms import ServiceBookingForm, TimeSlotSelectionForm
from services.models import (SpaService, Availability, TimeSlot,
                             SpecificDate, TimeSlotAvailability)


def book_spa_service(request):
    """
    Handles the booking of spa services.

    This view allows users to book a spa service
    by selecting a service, date, and quantity
    (only relevant for spa_access).
    It displays a form for selecting the spa service
    and date, and another form for selecting
    the time slot. If the form is submitted with
    valid data, it fetches the available time slots
    for the selected service and date, and calculates
    the price and access information.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the
        rendered booking page.

    Context:
        form (ServiceBookingForm): The form for
        selecting the spa service and date.
        time_slot_form (TimeSlotSelectionForm):
        The form for selecting the time slot.
        service_id (int or None): The ID of the
        selected spa service, if any.
        selected_date (datetime.date or None):
        The selected date, if any.
        quantity (int or None): The quantity of
        the selected service, if any.
        available_time_slots (QuerySet): The available
        time slots for the selected service and date.
        price (Decimal or None): The price of the selected
        service, if any.
        is_access (bool or None): The access information of
        the selected service, if any.
    """

    form = ServiceBookingForm()
    time_slot_form = TimeSlotSelectionForm()
    selected_service = None
    selected_date = None
    quantity = None
    available_time_slots = []
    unavailable_time_slots = []
    price = None
    is_access = None

    if request.method == "POST":
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            selected_service = form.cleaned_data.get("service")
            selected_date = form.cleaned_data.get("date")
            quantity = form.cleaned_data.get("quantity")

            if selected_service:
                price = selected_service.price
                is_access = selected_service.is_access

                specific_date = SpecificDate.objects.filter(
                    date=selected_date
                ).first()

            if selected_service and selected_date:

                specific_date = SpecificDate.objects.filter(
                    date=selected_date
                    ).first()
                specific_date = SpecificDate.objects.filter(
                    date=selected_date
                    ).first()
                if specific_date:
                    all_time_slots = TimeSlot.objects.filter(
                        spa_service=selected_service
                    ).distinct()

                    available_time_slots = TimeSlotAvailability.objects.filter(
                        availability__spa_service=selected_service,
                        specific_date=specific_date,
                        is_available=True
                    ).select_related('time_slot').order_by('time_slot__time')

                    unavailable_time_slots = TimeSlotAvailability.objects \
                        .filter(
                         availability__spa_service=selected_service,
                         specific_date=specific_date,
                         is_available=False
                        ).select_related('time_slot').order_by('time_slot__time')

                    available_time_slots = [
                        tsa.time_slot for tsa in available_time_slots
                    ]
                    unavailable_time_slots = [
                        tsa.time_slot for tsa in unavailable_time_slots
                        ]

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
            "unavailable_time_slots": unavailable_time_slots,
            "price": price,
            "is_access": is_access,
        },
    )
