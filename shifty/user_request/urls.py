from django.urls import path
from . import views

urlpatterns = [
	path('', views.userdata_request, name = "userdata_request")
]
