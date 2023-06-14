from .cart import Cart

def cart(request):
    # context processor for cart
    return {"cart":Cart(request)}