from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail

from services.models import Review 

from .forms import ContactForm

# Create your views here.


def index(request):
    """
    Render the index page of The Spa Stockholm.

    This view renders the index page, which serves as
    the main entry point for visitors to The Spa Stockholm's
    website. It retrieves context data using utility functions
    to display booking information and available spa services.

    The `book_spa_service` function is called to populate the
    'booking_context' variable, providing information about
    current spa service bookings or availability.

    The `spa_services` function is called to populate the
    'services_context' variable, providing details about
    the spa's available services, packages, and treatments.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered
        index page, displaying booking information and spa services.
    """
    booking_context = book_spa_service(request)
    services_context = spa_services(request)

    context = {
        'booking_context': booking_context,
        'spa_services': spa_services,
    }

    return render(request, 'home/index.html', context)


def contact(request):
    """
    Handle the contact form submission.

    This view processes the contact form, which allows
    users to send messages to the spa. If the request method is POST,
    it validates the form data and, if valid, sends an email
    containing the message details to the spa's email address.
    After a successful form submission, the user is redirected to
    a success page.

    If the request method is GET, it initialises an empty contact
    form and renders the contact page with the form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered
        contact page or a redirect to the success page.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                'Contact Form Submission',
                f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return HttpResponseRedirect(reverse('contact_success'))
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})


def contact_success(request):
    """
    Render the contact form submission success page.

    This view handles the HTTP GET request to display
    the contact form submission success page.
    After successfully submitting the contact form on
    the spa's website, users are redirected
    to this page to inform them that their message
    has been successfully sent.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with
        the rendered contact success page.
    """
    return render(request, 'home/contact_success.html')


def about(request):
    """
    Render the "About The Spa Stockholm" page.

    This view handles the HTTP GET request to display
    the "About The Spa Stockholm" page, which provides
    detailed information about the spa's philosophy,
    facilities, treatments, exclusive packages, commitment
    to service, and career opportunities.

    The HTML template 'spa/about.html' is used to render
    this page, containing comprehensive content that informs
    visitors about the spa and encourages potential employees
    to join the team.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with
        the rendered "About The Spa Stockholm" page.
    """
    return render(request, 'home/about.html')
