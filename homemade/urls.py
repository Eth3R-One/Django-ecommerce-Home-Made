from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# from django.contrib.admin.views.decorators import staff_member_required
from dashboard import urls as dashboard_urls

urlpatterns = [
    # path('dashboard/', include(dashboard_urls)),
    path('admin/', admin.site.urls),
    path('dashboard/',include('dashboard.urls')),
    path('', include('user.urls')),
    path('store/', include('store.urls')),
    path('', views.home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)