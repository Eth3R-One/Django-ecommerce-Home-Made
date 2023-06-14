from django import forms
from django.forms import ModelForm

from store.models import Product, Category, Order, OrderItem

# class TaskForm(forms.ModelForm):
#     title = forms.CharField(max_length=200, widget= forms.Textarea(attrs={'placeholder':'Enter new task here. . .'}))

#     class Meta:
#         model = Task
#         fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['slug', 'created_at', 'updated_at', 'user', 'thumbnail']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['slug', 'created_at', 'updated_at']


class UpdateOrderForm(forms.Form):
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES)
    is_paid = forms.BooleanField(required=False)
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_CHOICES)
    class Meta:
        mode = Order
        fields = ['status', 'is_paid', 'payment_method']
        labels = {
            'status': 'Status',
            'is_paid': 'Is Paid',
            'payment_method': 'Payment Method',
        }
        widgets = {
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input', 'value': 'True'}),
        }

