from collections import defaultdict

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import (
    render, get_object_or_404, redirect, reverse, HttpResponseRedirect
)

from .forms import reviewForm, FrontendTimeSlotForm
from .models import (
    SpaService, ServiceCategory, Review, Availability,
    TimeSlotAvailability, TimeSlot
)

# Create your views here.


def services_by_category(request, category_id):
    """
    Fetches spa services belonging to a specific service
    category and renders them in the index.html template.
    """

    category = get_object_or_404(ServiceCategory, id=category_id)
    services = SpaService.objects.filter(category=category)

    context = {
        "category": category,
        "services": services,
    }

    return render(request, "home/index.html", context)


def spa_services(request, context_only=False):
    """
    Fetches and optionally renders SpaService objects
    and ServiceCategory objects.
    """
    services = SpaService.objects.annotate(
        review_count=Count('reviews', filter=Q(reviews__approved=True))
    )
    access_services = services.filter(is_access=True)
    spa_services = services.filter(is_access=False)
    categories = ServiceCategory.objects.all()

    context = {
        "access_services": access_services,
        "spa_services": spa_services,
        "categories": categories,
    }

    if context_only:
        return context
    else:
        return render(request, "home/index.html", context)


def service_details(request, service_id):
    """
    Render the details of a specific spa service, including
    reviews.
    """
    service = get_object_or_404(SpaService, id=service_id)
    reviews = service.reviews.all().order_by("-created_on")
    review_count = service.reviews.filter(approved=True).count()

    if request.method == "POST":
        review_form = reviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.spa_service = service
            review.save()

            messages.add_message(
                request, messages.SUCCESS,
                'Review submitted and awaiting approval'
            )
            return redirect('service_details', service_id=service_id)
    else:
        review_form = reviewForm()

    return render(
        request,
        "services/services_details.html",
        {
            "service": service,
            "reviews": reviews,
            "review_count": review_count,
            "review_form": review_form,
        }
    )


def review_edit(request, service_id, review_id):
    """
    View to edit reviews.
    """
    if request.method == "POST":

        queryset = SpaService.objects.filter(status=1)
        spa_service = get_object_or_404(queryset, id=service_id)
        review = get_object_or_404(Review, pk=review_id)
        review_form = reviewForm(data=request.POST, instance=review)

        if review_form.is_valid() and review.author == request.user:
            review = review_form.save(commit=False)
            review.spa_service = spa_service
            review.approved = False
            review.save()
            messages.add_message(
                request, messages.SUCCESS, 'Review updated!'
            )
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating review!'
            )

    return HttpResponseRedirect(reverse('service_details', args=[service_id]))


def review_delete(request, service_id, review_id):
    """
    View to delete review. From Blog walkthrough.
    """
    queryset = SpaService.objects.filter(status=1)
    spa_service = get_object_or_404(queryset, id=service_id)
    review = get_object_or_404(Review, pk=review_id)

    if review.author == request.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own review!'
        )

    return redirect('service_details', service_id=service_id)


# Frontend Admin

@staff_member_required
def availability_overview(request):
    """
    Overview of availability.
    """
    availabilities = Availability.objects.all()
    return render(
        request,
        'admin/services/availability/availability_overview.html',
        {'availabilities': availabilities}
    )


@staff_member_required
def manage_time_slots_frontend(request, availability_id=None):
    """
    View for managing time slots.
    """
    spa_service_id = request.GET.get('spa_service')
    if spa_service_id:
        availability = get_object_or_404(Availability, spa_service_id=spa_service_id)
    else:
        availability = get_object_or_404(Availability, id=availability_id)

    if request.method == 'POST':
        form = FrontendTimeSlotForm(request.POST, availability=availability)
        if form.is_valid():
            form.save()

            unchecked_time_slot_ids = request.POST.getlist('unchecked_time_slots')
            if unchecked_time_slot_ids:
                TimeSlotAvailability.objects.filter(
                    availability=availability,
                    time_slot_id__in=unchecked_time_slot_ids,
                    specific_date=form.cleaned_data['specific_date']
                ).update(is_available=False, is_booked=False)

            messages.success(request, "Time slots have been successfully updated.")

            return redirect(reverse('manage_time_slots_frontend', args=[availability.id]))
        else:
            messages.error(request, "There was an issue updating the time slots. Please check your input.")
    
    else:
        specific_date = request.GET.get('specific_date')
        form = FrontendTimeSlotForm(availability=availability, initial={'specific_date': specific_date})

    spa_services = SpaService.objects.all()

    return render(
        request,
        'admin/services/availability/manage_time_slots.html',
        {
            'form': form,
            'availability': availability,
            'spa_services': spa_services,
        }
    )


@staff_member_required
def get_time_slots_for_date(request, availability_id):
    """
    Retrieves the list of time slots for a specific spa service
    on a given date.
    """
    try:
        date_id = request.GET.get('date_id')
        print(f"Date ID: {date_id}, Availability ID: {availability_id}")

        availability = get_object_or_404(Availability, id=availability_id)
        print(f"Found Availability: {availability}")

        all_time_slots = TimeSlot.objects.filter(
            spa_service=availability.spa_service
        )
        print(f"All Time Slots: {all_time_slots.count()}")

        available_time_slots = TimeSlotAvailability.objects.filter(
            availability=availability,
            specific_date_id=date_id
        )

        time_slots_data = []
        for time_slot in all_time_slots:
            availability_record = available_time_slots.filter(
                time_slot=time_slot
            ).first()
            is_available = (
                availability_record.is_available if availability_record
                else False
            )
            is_booked = (
                availability_record.is_booked if availability_record
                else False
            )

            time_slots_data.append({
                'time_slot__id': time_slot.id,
                'time_slot__time': time_slot.time,
                'is_available': is_available,
                'is_booked': is_booked,
            })
        print(f"Time Slots Data: {time_slots_data}")

        data = {
            'time_slots': time_slots_data
        }

        return JsonResponse(data)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
