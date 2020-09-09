"""shifty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from main_menu.views import HomeView
from attendance.views import RegisterView, CheckinView, CheckoutView, RFIDView
from doorbell.views import Doorbell

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.home, name='home'),
    path('register', RegisterView.register, name='register'),
    path('rfid_register', RegisterView.rifd_register, name='rfid_register'),
    path('registration_success', RegisterView.success, name='registration_success'),
    path('checkin', CheckinView.checkin, name='checkin'),
    path('checkin_success', CheckinView.success, name='checkin_success'),
    path('checkout', CheckoutView.checkout, name='checkout'),
    path('checkout_success', CheckoutView.success, name='checkout_success'),
    path('doorbell', Doorbell.doorbell, name='doorbell'),
    path('rfid', RFIDView.rfid_endpoint, name='rfid')

]
