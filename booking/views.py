from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .forms import ServiceBookingForm
from .models import SpaService
from services.models import Availability


# Create your views here.

def book_spa_service(request):
    available_time_slots = []
    selected_service = None
    selected_date_and_time = None

    if request.method == "POST":
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            selected_service = form.cleaned_data["service"]
            selected_date_and_time = form.cleaned_data["date_and_time"]
            availability = Availability.objects.filter(
                spa_service=selected_service,
                specific_dates__date=selected_date_and_time.date(),
            ).first()
            if availability:
                available_time_slots = availability.time_slots.all()
    else:
        form = ServiceBookingForm()

    return render(
        request,
        "booking/book_spa_service.html",
        {
            "form": form,
            "available_time_slots": available_time_slots,
            "service_id": selected_service.id if selected_service else None,
            "selected_service": selected_service,
            "selected_date_and_time": selected_date_and_time,
        },
    )
