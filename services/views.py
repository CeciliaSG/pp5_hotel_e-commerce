from django.shortcuts import render, get_object_or_404
from .models import SpaService, ServiceCategory


# Create your views here.


def services_by_category(request, category_id):
    """
    Fetches spa services belonging to a specific service category and renders them in the index.html template.

    Retrieves the ServiceCategory object identified by the provided category_id from the database. 
    Filters SpaService objects based on the retrieved category to fetch all services associated with that category.

    Args:
        request (HttpRequest): The HTTP request object.
        category_id (int): The ID of the ServiceCategory to filter SpaService objects.

    Returns:
        HttpResponse: Rendered response with the index.html template displaying spa services 
                      belonging to the specified service category.

    Raises:
        Http404: If the ServiceCategory with the given category_id does not exist.

    Usage:
        This view is typically used to display spa services categorized under specific ServiceCategory objects 
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
    Fetches and optionally renders SpaService objects and ServiceCategory objects.

    Retrieves all SpaService objects from the database. Filters these objects into 'access_services'
    (services that require special access) and 'spa_services' (standard spa services).

    Also retrieves all ServiceCategory objects to categorize the spa services.

    Args:
        request (HttpRequest): The HTTP request object.
        context_only (bool, optional): If True, returns a dictionary context containing access_services,
                                       spa_services, and categories without rendering a template. Defaults to False.

    Returns:
        HttpResponse or dict: If context_only is False, renders the 'home/index.html' template with context data
                              containing access_services, spa_services, and categories. If context_only is True,
                              returns a dictionary context with the same data.

    Usage:
        This view is typically used to display various spa services categorized by access type and ServiceCategory
        on the index or home page of a spa website.

    """
    services = SpaService.objects.all()

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
    Render the details of a specific spa service.

    Retrieves a SpaService object from the database based on the provided service_id.
    If the service_id does not exist, a HTTP 404 Not Found error is raised.

    Args:
        request (HttpRequest): The HTTP request object.
        service_id (int): The ID of the SpaService to retrieve details for.

    Returns:
        HttpResponse: Rendered template 'services/service_details.html' displaying details
                      of the retrieved SpaService.

    Usage:
        This view is typically used to display detailed information about a specific spa service
        on a dedicated service details page in a spa website.
    """

    service = get_object_or_404(SpaService, id=service_id)
    return render(request, 'services/services_details.html', {'service': service})
