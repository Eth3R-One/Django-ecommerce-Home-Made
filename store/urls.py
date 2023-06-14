from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('search/',views.search, name='search'),
    path('add-to-cart/<str:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/',views.checkout, name='checkout'),
    path('<slug:slug>/', views.product_details, name='product_details'),
    path('<int:id>/', views.product_details_by_id, name='product_details_by_id'),
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('change-quantity/<str:product_id>/', views.change_quantity, name='change-quantity'),



    path('payment/<uuid:uid>/', views.payment, name='payment'),
    # path('payment-complete/<uuid:uid>/', views.payment_complete,name='payment-complete'),


    # path('dashboard/', include('dashboard.urls')),

]
