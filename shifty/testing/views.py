from django.shortcuts import render
from django.http.response import HttpResponse
import os

def testing(request):
	if request.method == "POST":
		os.system(f"wall 'hello bendik, this is a post: {request}'")
		print(f"POST req: {request}")
	elif request.method == "GET":
		os.system(f"wall 'Yo bendik, this is a get: {request}'")
		print(f"GET req: {request}")

	return HttpResponse(status=418)
# Create your views here.
