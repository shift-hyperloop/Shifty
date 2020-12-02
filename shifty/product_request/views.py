from django.http import HttpResponse
import random
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from internal_kiosk_website.models import Products

@csrf_exempt
def product_request(request):

    if request.method == "GET":
        # Two parameters passed through the request
        barcode = request.GET.get("barcode")
        number_purchased = int(request.GET.get("bought"))
        safety_key = request.GET.get("key")

        if barcode and safety_key and number_purchased!=None:  # Check if all necessary parameters were passed
            if safety_key == "elonsmusk":  # Check if the correct safety key has been used

                try:
                    item = Products.object.get(barcode=barcode)
                    if number_purchased > 0:
                        item.amount -= number_purchased
                        item.save()
                    return HttpResponse(f"{barcode},{item.name},{item.price},{item.amount}")

                except Products.DoesNotExist:

                    while 1:
                        random_id = random.randint(100, 300)  # Set random id
                        try: 
                            Products.object.get(name=str(random_id))  # check if id exists

                        except Products.DoesNotExist:
                            # user can update name through slack
                            Products.object.create(name=str(random_id), price=0, amount=0, barcode=barcode)  # create item in database with id
                            return HttpResponse(str(random_id))  # return the id with a negative sign

            else:
                response="-1" #return -1 if safety key is wrong
        else:	
            response="-1" #return -1 if somehting was forgotten
        return HttpResponse(response)
    if request.method == "POST":
        print("hello")   
        print(request.POST) 
        print(request.POST.getlist("product"))
        return HttpResponse(status=201)    
    

        # else:	
        #     return HttpResponse("-1")  # return -1 if something was forgotten
