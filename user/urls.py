from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from core.models import Store_components
logo = Store_components.objects.last()

urlpatterns = [
    path('signup/', views.sign_up, name= 'signup'),
    # path('login/', auth_views.LoginView.as_view(template_name = 'user/login.html', redirect_authenticated_user = True,extra_context = {"logo":logo}), name= 'login'),
    path('login/', views.user_login, name= 'login'),
    path('profile/', views.profile, name = 'profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('my-orders/', views.orders, name='orders'),
    path('my-orders/<uuid:order_id>/', views.order_details, name='order-details'),
]
