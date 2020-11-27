from django.urls import path
from . import views

urlpatterns = [
	path('', views.product_request, name = "product_request")
]
