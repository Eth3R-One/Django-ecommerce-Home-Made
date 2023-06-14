# checkout form
# we will use the same form for both checkout and order update

from django import forms
from .models import Order
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "address",
            "phone_number",
            "payment_method",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Phone Number"}
            ),
            # "payment_method": forms.Select(attrs={"class": "form-control"}),

        }

        def __init__(self, *args, **kwargs):
            super(CheckoutForm, self).__init__(*args, **kwargs)
            self.fields["payment_method"].label = "Payment Method"
            self.fields["payment_method"].required = True
            self.fields["phone"].required = True
            self.fields["place"].required = True
            self.fields["address"].required = True
            self.fields["first_name"].readonly = True
            self.fields["last_name"].readonly = True
