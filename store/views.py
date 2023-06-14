from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse

from django.db.models import Q
from .models import Product, Order, Category, OrderItem
from .cart import Cart
from .forms import CheckoutForm

from core.models import Store_components

# Create your views here.
from core.models import Store_components

logo = Store_components.objects.last()
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def product_details(request, slug):
    logo = Store_components.objects.last()
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "logo": logo,
        },
    )


def product_details_by_id(request, pk):
    logo = Store_components.objects.last()
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "logo": logo,
        },
    )


def search(request):
    query = request.GET.get("query", "")
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    return render(
        request,
        "store/search.html",
        {
            "query": query,
            "products": products,
            "logo": logo,
        },
    )


def cart_view(request):
    cart = Cart(request)
    return render(
        request,
        "store/cart_view.html",
        {
            "title": "Cart",
            "cart": cart,
            "logo": logo,
        },
    )


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    product = Product.objects.get(pk=product_id)
    messages.info(request, f"{product.title} added to cart.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.info(request, "Item removed from cart.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


def change_quantity(request, product_id):
    action = request.GET.get("action", "")
    if action:
        quantity = 1
        if action == "minus":
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login")
def checkout(request):
    cart = Cart(request)
    if cart.get_total_quantity() == 0:
        return redirect("cart_view")
    form = CheckoutForm()
    user = request.user
    profile = user.userprofile
    if user.first_name:
        form.fields["first_name"].initial = user.first_name
    if user.last_name:
        form.fields["last_name"].initial = user.last_name
    if profile.address:
        form.fields["address"].initial = profile.address
    if profile.phone_number:
        form.fields["phone_number"].initial = profile.phone_number

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            order1 = Order.objects.create(
                user=user,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                address=form.cleaned_data.get("address"),
                phone_number=form.cleaned_data.get("phone_number"),
                payment_method=form.cleaned_data.get("payment_method"),
            )
            cart = Cart(request)
            # print(cart)
            for item in cart:
                # print(item)
                order_item = OrderItem.objects.create(
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["total_price"]/item["quantity"],
                    order=order1,
                )
                order_item.save()
            cart.clear()
            return redirect(reverse("payment", args=[order1.uid]))
    return render(
        request,
        "store/checkout.html",
        {
            "title": "Checkout",
            "logo": logo,
            "form": form,
        },
    )


def payment(request, uid):
    order = get_object_or_404(Order, uid=uid)
    if order.is_paid:
        return redirect("orders")
    messages.success(request, "Successfully placed the order!")
    return render(
        request,
        "store/payment.html",
        {
            "title": "Payment",
            "logo": logo,
            "order": order,
        },
    )
