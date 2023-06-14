from django.shortcuts import render

from store.models import Product
# Create your views here.
from core.models import Store_components
def home(request):
    logo = Store_components.objects.last()
    products = Product.objects.all()
    return render(request,'store/home.html', {'products':products, 'logo':logo})