from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from annoying.functions import get_object_or_None
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


import random
import re
import threading

## import models
from attendance.models import RFIDUser
from internal_kiosk_website.models import Products
import kiosk_endpoint.kiosk_logging


class KioskBackend:

    @staticmethod
    @csrf_exempt
    def kiosk_endpoint(request):
        """
        Send data to db with POST
        get data from db with GET
        An event needs to be defined for both of these 
        requests.
        The events are, for POST: "add to balance", "subtract balance", "log"
                        for GET:  "get product", "get user"
        """
        if request.method == "POST":
            kiosk_event = request.POST.get("event")
            rfid = request.POST.get("rfid", None)

            if kiosk_event == "add to balance":
                try:
                    # Get the number to add to balance
                    add_to_balance = abs(int(request.POST.get("balance", 0)))
                except ValueError:
                    # If the value inserted cant be converted to a number
                    print("Cannot convert balance to number")
                    return HttpResponse(status = 400)
                KioskBackend.user_balance(rfid, add_to_balance)

            elif kiosk_event == "subtract balance":
                try:
                    # Get the number to add to balance
                    subtract_from_balance = -abs(int(request.POST.get("balance", 0)))
                except ValueError:
                    # If the value inserted cant be converted to a number
                    print("Cannot convert balance to number")
                    return HttpResponse(status = 400)
                KioskBackend.user_balance(rfid, subtract_from_balance)

            elif kiosk_event == "finish_purchase":
                """
                Creates a dict from the data we get
                example:
                logging_object = {
                                    coke: {"price":10,"barcode":"312312312", "stock_change":1,
                                    "user_balance_after":20, "user_balance_before":30,
                                    "username":buddha, "stock_before_change":999, 
                                    "stock_after_change":998}
                                }
                """
                barcodes = request.POST.getlist("barcode", None)
                rfid = request.POST.get("rfid", None)
                user = RFIDUser.objects.get(rfid = rfid)

                logging_object = {}
                for barcode in barcodes:
                    product = get_object_or_None(Products,barcode = barcode)

                    if product.name in logging_object:
                        logging_object[product.name]["stock_change"] += 1
                    else:
                        logging_object[product.name]=dict()
                        logging_object[product.name]["price"] = product.price
                        logging_object[product.name]["stock_before_change"] = product.amount
                        logging_object[product.name]["barcode"] = product.barcode
                        logging_object[product.name]["stock_change"] = 1
                        logging_object[product.name]["username"] = f"{user.given_name} {user.family_name}"
                        logging_object[product.name]["balance_before"] = user.kiosk_balance
                    
                #Get total price and convert into integer
                try:
                    total_price = int(request.POST.get("total_price", 0))
                    
                     #Change balance of user
                    KioskBackend.user_balance(rfid, total_price) #Subract from total
                except ValueError:
                    #something is wrong with the price input
                    total_price = f"ERROR!! {request.POST.get('total_price',0)}"
                # print(product)
                # Reduce the amount in stock
                for product in logging_object.keys():
                    KioskBackend.change_product_stock(logging_object[product]["barcode"], logging_object[product]["stock_change"])
                
                #Log user balance and product stock after changes
                user = RFIDUser.objects.get(rfid = rfid)
                for key in logging_object.keys():
                    product = get_object_or_None(Products,barcode = logging_object[key]["barcode"])
                    logging_object[key]["balance_after"] = user.kiosk_balance
                    logging_object[key]["stock_after_change"] = product.amount

                #Log everything
                # spawn a thread that can finish the logging while the main thread can give the post response
                # logging is a bit slow, which is why we need to spawn a new thread
                logging_thread = threading.Thread(target = KioskBackend.log_object,args=(logging_object,)) 
                logging_thread.start()

                return HttpResponse(status = 200) #Return all is good

            else:
                print("Event not recognized")
                return HttpResponse(status = 400) # Bad request
        elif request.method == "GET":
            ## send data to the front end
            event = request.GET.get("event")
            if event == "get_product":
                """
                Checks if product exists, if not registers in db with name as random id
                Otherwise the html will return
                "barcode, product name, price, number in stock"
                """
                barcode = request.GET.get("barcode")
                if barcode == None:
                    return HttpResponse("-1")
                else:
                    product = get_object_or_None(Products,barcode = barcode)
                    if product == None:
                        # barcode doesn't exist, register product in db with random id
                        # change product on internal website
                        id = KioskBackend.register_product(barcode)
                        return HttpResponse(id)
                    else:
                        return HttpResponse(f"{barcode},{product.name},{product.price},{product.amount}")

            elif event == "get_user":
                """
                Checks if user exists, if not registers in db with name as random id
                Otherwise the html will return
                "rfid, full name, balance"
                """
                rfid = request.GET.get("rfid")
                if rfid == None:
                    return HttpResponse("-1")
                else:
                    user = get_object_or_None(RFIDUser, rfid = rfid) 
                    if user == None:
                        # RFID code doesn't exist, register user in db with random id
                        # user can change name on website(?)
                        id = KioskBackend.register_user(rfid)
                        return HttpResponse(id)
                    else:
                        return HttpResponse(f"{rfid}, {user.given_name} {user.family_name}, {user.kiosk_balance}")

            else:
                return HttpResponse("-1") # Bad request

    
    @staticmethod
    def user_balance(rfid, balance_change:int):
        user = RFIDUser.objects.get(rfid = rfid)
        if user.kiosk_balance - balance_change >= 0:
            #balance change is negative if we subtract and positive if we add
            user.kiosk_balance -= balance_change
            user.save()
            return True
        else:
            # Use to tell frontend that something went wrong
            return False
        
    @staticmethod
    def register_user(rfid):
        """
        Registers rfid code with a random integer (100-300)
        Checks that the id isn't alreay given to another user
        return the id
        """
        while 1:
            random_id = str(random.randint(100, 300)) #set random id
            user = get_object_or_None(RFIDUser, given_name = random_id)
            if user == None:
                RFIDUser.objects.create(given_name=random_id, family_name="",email="", rfid=rfid, kiosk_balance=0) #create user in database with id
                return random_id
        
    @staticmethod
    def register_product(barcode):
        """
        Registers product for a given barcode with a random integer (100-300)
        Checks that the id isn't alreay given to another product
        return the id
        """
        while 1:
            random_id = str(random.randint(100, 300))
            product = get_object_or_None(Products, name = random_id) 
            if product == None:
                Products.object.create(name=random_id, price = 0, amount = 0, barcode = barcode) #create user in database with id
                return random_id
    
    @staticmethod
    def change_product_stock(barcode, change):
        product = get_object_or_None(Products,barcode = barcode)
        try:
            product.amount -= int(change)
            product.save()
        except ValueError:
            print("Value cannot be converted into integer")


    @staticmethod
    def log_object(data):
        for key in data.keys():
            kiosk_endpoint.kiosk_logging.log_everything(
                key, data[key]["username"],
                data[key]["stock_change"], data[key]["price"],
                data[key]["balance_before"], data[key]["balance_after"],
                data[key]["stock_before_change"], data[key]["stock_after_change"],
            )

class ProductOverview:
    #TODO:
    #Logging events
    #Deleting items

    @staticmethod
    # @login_required
    @csrf_exempt
    def load_page(request):
        if request.method == "POST":
            # Split data form into a dictionary for each product
            form_data = {}
            delete_list = []
            for key in request.POST.keys():
                if len(key.split("_"))!=2:
                    continue
                name, keyword = key.split("_")
                if name not in form_data:
                    form_data[name] = {}
                form_data[name][keyword] = request.POST[key]

            for name in form_data:
                #iterate though products: coke, daim, etc...
                product = Products.object.get(name = name)
                for key in form_data[name].keys():
                    #Look for change in parameters: name, price, stock, delete?
                    if form_data[name][key] == '':
                        #if no change, go to next
                        continue
                    if len(re.findall("[^A-Za-z0-9- !]", form_data[name][key])):
                        #Check for weird characters
                        continue
                    if key == "price":
                        #change price
                        product.price = int(form_data[name][key])
                    elif key == "stock":
                        #Change product stock
                        product.amount += int(form_data[name][key])
                    elif key == "delete":
                        #make product ready for deletion
                        #might change later but makes sense for now
                        delete_list.append(name)
                        break
                    elif key == "name":
                        #change product name
                        product.name = form_data[name][key]
                product.save()

            print(delete_list)

        if not request.user.is_authenticated:
            return redirect("/")

        context = {
            'prods': Products.object.all(),
            "base_template_name": "base_authenticated.html",
            
        }
        return render(request,'products.html',context)
                
class RegisterUser:

    @staticmethod
    def load_page(request):
        """
            load register user page
        """
        context = {"base_template_name": "base_authenticated.html"}
        if request.method == "POST":
            context["success"] = RegisterUser.register_user(request)
        
        if not request.user.is_authenticated:
            return redirect("/")

        return render(request, "register.html", context)

    @staticmethod
    def register_user(request):
        """
        get data from post request
        register user
        can only change a user already in the database, not create a new one.
        Automatic register with random id first time RFID scanned
        TODO: deny symbols in name and email
        """
        database_temp_id = request.POST.get("db_id")
        fullname         = request.POST.get("fullname").split() #Append empty string incase last name was forgotten
        if len(fullname) == 1: #if a last name is not given add an empty space
            fullname.append(" ")
        elif len(fullname) > 2: # If multiple names, add one first name, and the others as family name
            temp = [fullname[0]]
            temp.extend([name for name in fullname[1:]])

        email = request.POST.get("email")

        try:
            balance = int(request.POST.get("balance"))
        except ValueError:
            balance = 0

        user = get_object_or_None(RFIDUser, given_name = database_temp_id)
        if user:

            user.given_name  = fullname[0]
            user.family_name = fullname[1]

            user.kiosk_balance = balance
            user.email = email
            user.save()
            return 1

        return 0

class InsertThemCashMoney:
    
    @staticmethod
    def load_page(request):
        context={"base_template_name":"base_authenticated.html"}
        
        if not request.user.is_authenticated:
            return redirect("/")
        if request.method == "POST":
            name = request.POST.get("name")
            name = name.split(' ')
            name.append(" ")
            balance = int(request.POST.get("balance"))
            first_name = name[0]
            last_name = name[1]

            user = RFIDUser.objects.filter(given_name = first_name).filter(family_name = last_name)
            if user.exists():
                user = RFIDUser.objects.get(rfid = user[0].rfid)
                user.kiosk_balance += balance
                user.save()
                print(user.kiosk_balance+balance,user.kiosk_balance, balance)
                context["name"] = f"{user.given_name} {user.family_name}"
            else:
                context["error"] = 1
            
        return render(request, "money.html", context)

class DefaultHomePage:

    @staticmethod
    def load_page(request):
        context = {}
        if not request.user.is_authenticated:
            context["base_template_name"] = "base_not_auth.html"
        else:
            context["base_template_name"] = "base_authenticated.html"

        return render(request, "home.html", context)

# class StatisticView:

#     @staticmethod
#     def load_page(request):

def kiosk_website_login(request):
    if request.user.is_authenticated:
        return redirect("/")

    context = {"base_template_name":"base_not_auth.html"}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context["error"] = 1
    
    return render(request, "login.html", context)

class ExtraLog:
    """
    A way to directly read the local product log on the website
    """
    @staticmethod
    def load_page(request):
        if not request.user.is_authenticated:
            return redirect("/")

        local_log_file =  open("local_product_log.txt", 'r') 
        response = HttpResponse(local_log_file.read(), content_type='text/plain')
        response['Content-Disposition'] = 'inline;filename=local_product_log.txt'
        return response

class Statistics:
    @staticmethod
    def load_page(request):
        if not request.user.is_authenticated:
            return redirect("/")

        users_in_db = RFIDUser.objects.all()

        context={"base_template_name":"base_authenticated.html"}
        total = 0
        max_loops = 0
        for user in users_in_db:
            user_balance = user.kiosk_balance
            if user_balance > max_loops:
                max_loops = user_balance
                high_score = f"{user.given_name} {user.family_name}"
            total += user_balance


        context["total_loops"] = total
        context["highscore_name"] = high_score
        context["highscore_balance"] = max_loops
        return render(request, "statistics.html", context)