from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.
from internal_kiosk_website.models import Products


def product_request(request):
    if request.method == "GET":
        # Two parameters passed through the request
        barcode = request.GET.get("barcode")
        number_purchased = int(request.GET.get("bought"))
        safety_key = request.GET.get("key")
        print(barcode, safety_key)
        if barcode!= None and safety_key!=None and number_purchased!=None:
            if safety_key == "elonsmusk":  # Check if the correct safety key has been used
                try:
                    item = Products.object.get(barcode = barcode)
                    if number_purchased > 0:
                        item.amount -= number_purchased
                        item.save()
                    response = f"{barcode}, {item.name},{item.price},{item.amount}"
                except Products.DoesNotExist:
                    while 1:
                        random_id = random.randint(100, 300) #set random id
                        try: 
                            Products.object.get(name = f"random_id") #check if id exists
                        except:
                            # user can update name through slack
                            Products.object.create(name=f"{random_id}",price = 0, amount = 0, barcode=barcode) #create item in database with id
                            response = f"-{random_id}" #return the id with a negative sign
                            break
            else:
                response="-1" #return -1 if safety key is wrong
        else:	
            response="-1" #return -1 if something was forgotten
            
    return HttpResponse(response)
