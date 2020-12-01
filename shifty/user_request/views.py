from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.
from attendance.models import RFIDUser
from django.test import Client

def userdata_request(request):
	if request.method == "GET":
		# Three parameters passed through the request
		#rfid, amount used(can be 0), and a safety key(just for some sort of safety)
		rfid = request.GET.get("rfid")
		amount_used = int(request.GET.get("loops_used"))
		safety_key = request.GET.get("key")

		if safety_key == "elonsmusk": #Check if the correct safety key has been used
			try:
				user = RFIDUser.object.get(rfid = rfid) # try to get user from database using rfid code
				if amount_used > 0: 
					if user.kiosk_balance - amount_used >= 0:
						user.kiosk_balance -= amount_used ##Update the balance in the database
						user.save()
					else:
						response = "balance too low for purchase" # return error
				response = f"{rfid}, {user.given_name} {user.family_name},{user.kiosk_balance}" #response the request with the name and balance
			except RFIDUser.DoesNotExist: #if user doesnt exist
				while 1:
					random_id = random.randint(100, 300) #set random id
					try: 
						RFIDUser.object.get(given_name = f"random_id") #check if id exists
					except:
						#user can update name through slack
						RFIDUser.object.create(given_name=f"{random_id}", family_name="",phone_mnumber="",email="", rfid=rfid, kiosk_balance=0) #create user in database with id
						response = f"-{random_id}" #return the id with a negative sign
						break

						
		else:
			response="-1" #return -1 if safety key is wrong
	return HttpResponse(response)
	
	
