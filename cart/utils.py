def get_cart_from_session(request):
    """
    Retrieve cart data from session.
    """
    return request.session.get('cart', {})