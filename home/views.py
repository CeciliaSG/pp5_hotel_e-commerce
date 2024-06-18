from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import ContactForm


# Create your views here.

def index(request):
    """
    Renders index template
    """

    booking_context = book_spa_service(request)
    services_context = spa_services(request)

    context = {
        'booking_context': booking_context,
        'services_context': services_context,
    }

    return render(request, 'home/index.html', context)


def contact(request):
    return render(request, 'home/contact.html')

from .forms import ContactForm

def contact(request):
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
    return render(request, 'home/contact_success.html')