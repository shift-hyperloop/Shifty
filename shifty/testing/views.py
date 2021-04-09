import os

from django.shortcuts import render
from django.http.response import HttpResponse
from slack import WebClient
from django.views.decorators.csrf import csrf_exempt

from utils.logger import create_logger

@csrf_exempt
def testing(request):
	logger = create_logger()
	client = WebClient(token=os.environ.get('SLACK_API_TOKEN'))
	if request.method == "POST":
		user_id = request.POST['user_id']
		user_info = client.users_info(user=user_id)
		print(user_info)
		real_name = user_info['user']['profile']['real_name']
		email = user_info['user']['profile']['email'] 
		phone = user_info['user']['profile']['phone']

		print(f"Email: {email}")
		print(f'Phone: {phone}')
	elif request.method == "GET":
		os.system(f"wall 'Yo bendik, this is a get: {request}'")
		logger.debug(f"GET req: {request}")

	return HttpResponse(status=418)
# Create your views here.
