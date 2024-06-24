import json
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest

from booking.models import SpaBookingServices, SpaBooking, SpaService
from services.models import TimeSlot
from booking.forms import TimeSlotSelectionForm



# Create your views here.

def add_to_cart(request, service_id=None):


    """
    Adds a selected spa service to the cart.

    This view handles the addition of a spa service to the user's shopping cart.
    It verifies that a valid service ID is provided, checks the validity of the 
    submitted time slot form, and calculates the total price based on the selected 
    quantity and price. The service is then added to the session-based cart, which 
    can be viewed and modified by the user.

    Args:
        request (HttpRequest): The HTTP request object containing form data.
        service_id (int or None): The ID of the spa service to add to the cart.

    Returns:
        HttpResponse: A redirection to the 'view_cart' page upon successful addition,
                      or a redirection back to the booking page with error messages if 
                      the form is invalid.
        HttpResponseBadRequest: If required data is missing or invalid.

    Context:
        cart (dict): A dictionary stored in the session representing the cart.
        service_key (str): A unique key combining the service ID, selected date, and 
                           time slot ID to uniquely identify a cart item.

    Raises:
        HttpResponseBadRequest: If the service ID is not provided, the quantity is 
                                not an integer, the price is not a valid number, or 
                                other required fields are missing.
    """

    if service_id is None:
        return HttpResponseBadRequest("Service ID is required")

    selected_service = get_object_or_404(SpaService, pk=service_id)

    if request.method == "POST":

        time_slot_form = TimeSlotSelectionForm(request.POST)
        if not time_slot_form.is_valid():
            errors = time_slot_form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"Error in {field}: {error}", extra_tags='alert alert-danger')
            return redirect('book_spa_service')

        if time_slot_form.is_valid():
            selected_time_slot = time_slot_form.cleaned_data["selected_time_slot"]
            selected_date = request.POST.get("selected_date")
            quantity = request.POST.get("quantity")
            price = request.POST.get("price")

            if not selected_time_slot:
                messages.error(request, "You must select a time slot.", extra_tags='alert alert-danger')
                return redirect('book_spa_service')

            if not quantity:
                return HttpResponseBadRequest("Quantity is required")

            try:
                quantity = int(quantity)
            except ValueError:
                return HttpResponseBadRequest("Quantity must be an integer")

            try:
                price = float(price)
            except ValueError:
                return HttpResponseBadRequest("Price must be a valid number")

            try:
                spa_service_total = float(price) * quantity
            except ValueError:
                return HttpResponseBadRequest("Price must be a valid number")

            if selected_service.price is None:
                return HttpResponseBadRequest("Price for selected service is not defined")

            spa_service_total = selected_service.price if selected_service.price else 0

            cart = request.session.get("cart", {})
            service_key = f"{selected_service.id}_{selected_date}_{selected_time_slot.id}"
            
            if selected_service.is_access:
                if service_key in cart:
                    cart[service_key]["quantity"] += int(quantity)
                else:
                    cart[service_key] = {
                        "service_id": selected_service.id,
                        "spa_service": selected_service.name,
                        "quantity": int(quantity),
                        "spa_service_total": str(spa_service_total),
                        "selected_date": selected_date,
                        "selected_time": str(selected_time_slot.time),
                         "selected_time_slot_id": selected_time_slot.id,
                        "is_access": selected_service.is_access
                    }

            else:
                if service_key not in cart:
                    cart[service_key] = {
                        "service_id": selected_service.id,
                        "spa_service": selected_service.name,
                        "quantity": 1,  
                        "spa_service_total": str(spa_service_total),
                        "selected_date": selected_date,
                        "selected_time": str(selected_time_slot.time),
                        "selected_time_slot_id": selected_time_slot.id,
                        "is_access": selected_service.is_access
                    }
                else:
                    messages.warning(request, ('A service cannot be added more than once for the same date and time.'))
                    return redirect("book_spa_service")

            request.session["cart"] = cart
            request.session.modified = True
            return redirect("view_cart")

    return HttpResponseBadRequest("Invalid request, problem at the start")
    

def update_cart(request, service_id):
    """
        Updates the quantity of a specified spa service in the cart.

        This view handles the update of the quantity of a spa service in the user's 
        session-based cart. It finds the service in the cart by its ID, updates 
        the quantity, recalculates the total price for that service, and saves the updated 
        cart back to the session.

        Args:
            request (HttpRequest): The HTTP request object containing form data.
            service_id (int): The ID of the spa service to update in the cart.

        Returns:
            HttpResponse: A redirection to the 'view_cart' page upon successful update.
            HttpResponseBadRequest: If the service is not found in the cart or the request 
                                    method is not POST.

        Context:
            cart (dict): A dictionary stored in the session representing the shopping cart.
            service_key (str): A unique key combining the service ID, selected date, and 
                            time slot ID to uniquely identify a cart item.

        Raises:
            HttpResponseBadRequest: If the service is not found in the cart.
    """

    if request.method == "POST":
        cart = request.session.get("cart", {})
        for key in cart.keys():
            if str(service_id) in key:
                new_quantity = int(request.POST.get("quantity", 1))
                cart[key]["quantity"] = new_quantity
                cart[key]["spa_service_total"] = str(float(cart[key]["spa_service_total"]) / cart[key]["quantity"] * new_quantity)
                request.session["cart"] = cart
                request.session.modified = True
                break
        else:
            return HttpResponseBadRequest("Service not found in cart")
    return redirect("view_cart")


def view_cart(request):
    """
    Displays the contents of the cart.

    This view retrieves the user's session-based shopping cart, calculates the 
    total cost of the services in the cart, and renders the cart contents on the 
    'view_cart.html' template. It handles the session data for the cart, ensuring 
    that each service's details and total cost are correctly computed and passed 
    to the template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered 'view_cart.html' 
                      template displaying the cart contents and total cost.

    Context:
        services (list): A list of dictionaries representing the services in the cart. 
                         Each dictionary contains:
                         - id (str): The unique identifier for the cart item.
                         - spa_service (str): The name of the spa service.
                         - quantity (int): The quantity of the service.
                         - spa_service_total (Decimal): The total cost for the service.
                         - selected_date (str): The selected date for the service.
                         - selected_time (str): The selected time for the service.
                         - selected_time_slot_id (int): The ID of the selected time slot.
                         - is_access (bool): Indicates if the service is an accessibility 
                                             service.
        total_cost (Decimal): The total cost of all services in the cart.
    """

    cart = request.session.get("cart", {})
    services = []
    total_cost = Decimal("0.00")

    for service_id, details in cart.items():
        try:
            service_total = Decimal(details["spa_service_total"]) * details["quantity"]
            total_cost += service_total

            services.append(
                        {
                            "id": service_id,
                            "spa_service": details["spa_service"],
                            "quantity": details["quantity"],
                            "spa_service_total": service_total,
                            "selected_date": details["selected_date"],
                            "selected_time": details["selected_time"],                    
                            "selected_time_slot_id": details.get("selected_time_slot_id"),
                            "is_access": details.get("is_access", False)
                        }
            )
        except KeyError as e:
                    print(f"Missing key in cart session data: {e}")
        except TimeSlot.DoesNotExist:
                    print(f"TimeSlot with id {details.get('selected_time_slot_id')} does not exist.")    

    context = {
        "services": services,
        "total_cost": total_cost,
    }
    return render(request, "cart/view_cart.html", context)


def remove_from_cart(request, service_id):
    """
    Remove a specific service from the cart.

    This view handles the removal of a service from the user's session-based shopping cart. 
    If the specified service ID exists in the cart, it will be removed. If the service ID 
    does not exist, an error message will be displayed. After attempting to remove the 
    service, the user is redirected to the 'view_cart' page, with a success or error 
    message depending on the outcome.

    Args:
        request (HttpRequest): The HTTP request object.
        service_id (int or str): The unique identifier of the service to be removed from 
                                 the cart.

    Returns:
        HttpResponse: A redirect to the 'view_cart' page with a success or error message.

    """

    cart = request.session.get("cart", {})
    try:
        if str(service_id) in cart:
            del cart[str(service_id)]
            messages.success(request, "Service removed from cart successfully")
        else:
            messages.error(request, "Service not found in cart")

        request.session["cart"] = cart
        return redirect("view_cart")

    except KeyError:
        messages.error(request, "Service not found in cart")
        return redirect("view_cart")


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

    request.session["cart"] = {}
    return redirect("view_cart")
