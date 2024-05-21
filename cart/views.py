from django.shortcuts import render, get_object_or_404, redirect
from booking.forms import SpaBookingForm, SpaBookingServicesFormSet
from booking.models import SpaBookingServices, SpaBooking
from decimal import Decimal

# Create your views here.

def add_to_cart(request, booking_id):
    booking = get_object_or_404(SpaBooking, pk=booking_id)
    cart = request.session.get('cart', {})

    cart.clear()
    booking_services = SpaBookingServices.objects.filter(spa_booking=booking)
    for service in booking_services:
        service_id = str(service.id)
        cart[service_id] = {
            'spa_service': service.spa_service.name,
            'quantity': service.quantity,
            'spa_service_total': str(service.spa_service_total)
        }

    print("Cart after adding services:", cart)
    
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