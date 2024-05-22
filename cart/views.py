from django.shortcuts import render, get_object_or_404, redirect
from booking.forms import SpaBookingForm, SpaBookingServicesFormSet
from booking.models import SpaBookingServices, SpaBooking
from decimal import Decimal

# Create your views here.

def add_to_cart(request, booking_id=None):
    if 'booking_id' in request.session:
        booking_id = request.session['booking_id']
    else:
        return redirect('book_spa_service')

    booking = get_object_or_404(SpaBooking, pk=booking_id)

    cart = request.session.get('cart', {})
    booking_services = SpaBookingServices.objects.filter(spa_booking=booking)
    for service in booking_services:
        service_id = str(service.id)
        if service_id in cart:
            cart[service_id]['quantity'] += service.quantity
        else:
            cart[service_id] = {
                'spa_service': service.spa_service.name,
                'quantity': service.quantity,
                'spa_service_total': str(service.spa_service_total)
            }

    request.session['cart'] = cart
    return redirect('view_cart')


def update_cart(request, service_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(service_id) in cart:
            new_quantity = int(request.POST.get('quantity', 1))
            cart[str(service_id)]['quantity'] = new_quantity
            request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    services = []
    total_cost = Decimal('0.00')

    for service_id, details in cart.items():
        try:
            service_total = Decimal(details['spa_service_total']) * details['quantity']
            total_cost += service_total
            services.append({
                'id': service_id,
                'spa_service': details['spa_service'],
                'quantity': details['quantity'],
                'spa_service_total': service_total
            })
        except KeyError as e:
            print(f"Missing key in cart session data: {e}")

    context = {
        'services': services,
        'total_cost': total_cost,
    }
    return render(request, 'cart/view_cart.html', context) 


def remove_from_cart(request, service_id):
    """
    Remove a specific service from the cart.
    """
    cart = request.session.get('cart', {})
    if service_id in cart:
        del cart[service_id]
    request.session['cart'] = cart
    return redirect('view_cart')


def clear_cart(request):
    """
    Clears all items from the user's cart stored in the session.

    This view sets the 'cart' key in the session to an empty dictionary,
    effectively removing all services that the user has added to the cart.
    After clearing the cart, the user is redirected to the view_cart page
    to see the updated (empty) cart.

    Used to generate the response.

    Returns:
        HttpResponseRedirect: A redirect response to the 'view_cart' page.
    """

    request.session['cart'] = {}
    return redirect('view_cart')