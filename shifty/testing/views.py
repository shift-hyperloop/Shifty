import os

from django.shortcuts import render
from django.http.response import HttpResponse
from slack import WebClient

def testing(request):
	client = WebClient(os.environ.get('SLACK_API_TOKEN'))
	if request.method == "POST":
		os.system(f"wall 'hello bendik, this is a post: {request}'")
		user_id = request.POST['user_id']
		user_info = client.users_info(user_id)
		real_name = user_info['real_name']
		email = user_info['profile']['email'] 

		print(f"POST req: {email}")
	elif request.method == "GET":
		os.system(f"wall 'Yo bendik, this is a get: {request}'")
		print(f"GET req: {request}")

	return HttpResponse(status=418)
# Create your views here.
