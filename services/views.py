from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import SpaService, ServiceCategory, Review, Availability, TimeSlotAvailability, TimeSlot
from django.contrib import messages
from .forms import reviewForm, FrontendTimeSlotForm
from collections import defaultdict

from django.db.models import Count, Q
from django.http import JsonResponse


# Create your views here.

def services_by_category(request, category_id):
    """
    Fetches spa services belonging to a specific service
    category and renders them in the index.html template.

    Retrieves the ServiceCategory object identified by the
    provided category_id from the database.
    Filters SpaService objects based on the retrieved category
    to fetch all services associated with that category.

    Args:
        request (HttpRequest): The HTTP request object.
        category_id (int): The ID of the ServiceCategory to
        filter SpaService objects.

    Returns:
        HttpResponse: Rendered response with the index.html template
        displaying spa services belonging to the specified service category.

    Raises:
        Http404: If the ServiceCategory with the given category_id does
        not exist.

    Usage:
        This view is typically used to display spa services categorized under
        specific ServiceCategory objects
        on the website's index or home page.
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

    Retrieves all SpaService objects from the database. Filters
    these objects into 'access_services'
    (services that require special access) and 'spa_services'
    (standard spa services).

    Also retrieves all ServiceCategory objects to categorize
    the spa services.

    Args:
        request (HttpRequest): The HTTP request object.
        context_only (bool, optional): If True, returns a dictionary
        context containing access_services,
        spa_services, and categories without rendering a template.
        Defaults to False.

    Returns:
        HttpResponse or dict: If context_only is False, renders
        the 'home/index.html' template with context data
        containing access_services, spa_services, and categories.
        If context_only is True, returns a dictionary context with
        the same data.

    Usage:
        This view is typically used to display various spa services
        categorized by access type and ServiceCategory
        on the index or home page of a spa website.

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
    Render the details of a specific spa service, including reviews.

    Retrieves a SpaService object from the database based on the provided
    service_id. If the service_id does not exist, a HTTP 404 Not Found error
    is raised. Handles review submission and displays reviews for the service.

    Args:
        request (HttpRequest): The HTTP request object.
        service_id (int): The ID of the SpaService to retrieve details for.

    Returns:
        HttpResponse: Rendered template 'services/service_details.html'
        displaying details of the retrieved SpaService, including reviews and
        a review form.

    Usage:
        This view is typically used to display detailed information about a
        specific spa service on a dedicated service details page in a spa website.
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
    view to edit reviews
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
            messages.add_message(request, messages.SUCCESS, 'review Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating review!')

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
            messages.add_message(request, messages.ERROR, 'You can only delete your own review!')

    return redirect('service_details', service_id=service_id)


@staff_member_required
def availability_overview(request):
    availabilities = Availability.objects.all()
    return render(request, 'admin/services/availability/availability_overview.html', {'availabilities': availabilities})


@staff_member_required
def manage_time_slots_frontend(request, availability_id=None):
    spa_service_id = request.GET.get('spa_service')
    if spa_service_id:
        availability = get_object_or_404(Availability, spa_service_id=spa_service_id)
    else:
        availability = get_object_or_404(Availability, id=availability_id)
    
    if request.method == 'POST':
        form = FrontendTimeSlotForm(request.POST, availability=availability)
        if form.is_valid():
            form.save()
            return redirect(reverse('manage_time_slots_frontend', args=[availability.id]))

    else:
        specific_date = request.GET.get('specific_date')
        form = FrontendTimeSlotForm(availability=availability, initial={'specific_date': specific_date})

    spa_services = SpaService.objects.all()

    return render(request, 'admin/services/availability/manage_time_slots.html', {
        'form': form,
        'availability': availability,
        'spa_services': spa_services,
    })



@staff_member_required
def get_time_slots_for_date(request, availability_id):
    date_id = request.GET.get('date_id')
    availability = get_object_or_404(Availability, id=availability_id)


    all_time_slots = TimeSlot.objects.filter(spa_service=availability.spa_service)

    available_time_slots = TimeSlotAvailability.objects.filter(
        availability=availability,
        specific_date_id=date_id
    )

    time_slots_data = []
    for time_slot in all_time_slots:
        time_slots_data.append({
            'time_slot__id': time_slot.id,
            'time_slot__time': time_slot.time,
            'is_available': available_time_slots.filter(time_slot=time_slot).exists()
        })

    data = {
        'time_slots': time_slots_data
    }

    return JsonResponse(data)





