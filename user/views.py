from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from core.models import Store_components
from .forms import UserRegisterForm, EmailAuthenticationForm, UpdateProfileForm, UpdateProfileForm2
from django.contrib.auth import authenticate
from django.contrib import messages
from store.models import Order, OrderItem


# Create your views here.

logo = Store_components.objects.last()


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print(form)
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            login(request, user)
            # userprofile = Userprofile.objects.create(user=user)
            messages.success(request, "User created successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Error creating your account!")

    else:
        form = UserRegisterForm()
    return render(request, "user/signup.html", {"form": form, "logo": logo})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, "Email dosen't exist!")
            return redirect("login")
        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "User logged in successfully!")
            return redirect("profile")
        else:
            messages.warning(request, "Error logging in!")
            return redirect("login")

    return render(
        request,
        "user/login.html",
        {
            "title": "Login",
            "logo": logo
        },
    )


@login_required
def profile(request):
    user = request.user
    title = "Profile "
    return render(
        request,
        "user/profile.html",
        {
            "user": user,
            "title": title,
            "logo": logo,
        },
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        form = UpdateProfileForm(request.POST, instance=user)
        form2 = UpdateProfileForm2(request.POST, instance=user.userprofile)
        email = request.POST["email"]
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        address = request.POST["address"]
        if (
            email == user.email
            and username == user.username
            and first_name == user.first_name
            and last_name == user.last_name
            and phone_number == user.userprofile.phone_number
            and address == user.userprofile.address
        ):
            messages.info(request, "No changes were made!")
            return redirect("profile")
        if form.is_valid() and form2.is_valid():
            non_valid_email = User.objects.filter(email=email).exclude(
                username=user.username
            )
            if email == None or email == "":
                messages.error(request, "Email is required!")
                return redirect("edit-profile")
            if non_valid_email:
                messages.error(request, "Email already exists!")
                return redirect("edit-profile")
            form.save()
            form2.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            non_valid_username = User.objects.filter(username=username).exclude(
                email=user.email
            )
            if non_valid_username:
                messages.error(
                    request,
                    "Username already exists! Try different username for now!!!",
                )
            else:
                messages.error(request, "Error updating your profile!")
            return redirect("edit-profile")
    form = UpdateProfileForm(instance=request.user)
    form2 = UpdateProfileForm2(instance=request.user.userprofile)

    return render(
        request,
        "user/edit_profile.html",
        {
            "form": form,
            "form2": form2,
            "logo": logo,
        },
    )

def orders(request):
    orders = Order.objects.filter(user = request.user).order_by('-created_at')
    orders_count = {}

    for order in orders:
        order_items = OrderItem.objects.filter(order=order).count()
        orders_count[order.uid] = order_items
    for key, value in orders_count.items():
        print("key:", key,"value: ", value)
    return render(request, 'user/orders.html', {
        "title": "Orders",
        "logo":logo,
        "orders":orders,
        "orders_count":orders_count,
    })

def order_details(request, order_id):
    order = get_object_or_404(Order, uid=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'user/order_details.html', {
        "title": "Order Details",
        "logo":logo,
        "order":order,
        "order_items":order_items,
    })