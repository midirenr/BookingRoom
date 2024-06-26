"""
URL configuration for Booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from RoomBooking import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/booking/view/', views.BookingView.as_view({'get': 'get_all_booking',
                                                            'post': 'get_detail_booking'})),
    path('api/v1/booking/create/', views.BookingCreate.as_view({'get': 'create_booking_view',
                                                                'post': 'create_booking'})),
    path('api/v1/booking/get_report/', views.BookingReport.as_view({'get': 'get_report_view',
                                                                    'post': 'get_report'})),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
