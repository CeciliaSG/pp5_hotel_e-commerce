from django.shortcuts import render, get_object_or_404
from .models import SpaService, ServiceCategory


# Create your views here.


def services_by_category(request, category_id):
    """
    Fetches and renders SpaServiceCategory in the index.html template
    """
    category = get_object_or_404(ServiceCategory, id=category_id)
    services = SpaService.objects.filter(category=category, available=True)

    print("Category:", Category)

    context = {
        'category': category,
        'services': services,
    }

    return render(request, 'home/index.html', context)


def spa_services(request):
    """
    Fetches and renders SpaServices in the index.html template
    """

    print("Executing spa_services view")

    services = SpaService.objects.filter(available=True)

    access_services = services.filter(is_access=True)
    spa_services = services.filter(is_access=False)
    categories = ServiceCategory.objects.all()

    print("Services:", services)
    print("Access Services:", access_services)
    print("Spa Services:", spa_services)
    print("Categories:", categories)

    context = {
        'access_services': access_services,
        'spa_services': spa_services,
        'categories': categories,
    }

    return render(request, 'home/index.html', context)