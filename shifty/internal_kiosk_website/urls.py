from django.urls import path
from django.conf.urls import re_path,url
from . import views
# from internal_kiosk_website.views import *



urlpatterns = [
	path("", views.index),
	path("/", views.index),
]
