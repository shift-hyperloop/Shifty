from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from annoying.functions import get_object_or_None

import random

## import models
from attendance.models import RFIDUser
from internal_kiosk_website.models import Products
import kiosk_endpoint.kiosk_logging


class KioskView:

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
                KioskView.user_balance(rfid, add_to_balance)

            elif kiosk_event == "subtract balance":
                try:
                    # Get the number to add to balance
                    subtract_from_balance = -abs(int(request.POST.get("balance", 0)))
                except ValueError:
                    # If the value inserted cant be converted to a number
                    print("Cannot convert balance to number")
                    return HttpResponse(status = 400)
                KioskView.user_balance(rfid, subtract_from_balance)

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
                user = RFIDUser.object.get(rfid = rfid)

                logging_object = {}
                for barcode in barcodes:
                    product = get_object_or_None(Products,barcode = barcode)
                    if logging_object[product.name]:
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
                    total_price = -abs(int(request.POST.get("total_price", 0)))
                except ValueError:
                    total_price = 0
                
                # Reduce the amount in stock
                for product in logging_object.keys():
                    KioskView.change_product_stock(logging_object[product]["barcode"], logging_object[product]["stock_change"])
                
                #Change balance of user
                KioskView.user_balance(rfid, total_price) #Subract from total

                #Log user balance and product stock after changes
                user = RFIDUser.object.get(rfid = rfid)
                for key in logging_object.keys():
                    product = get_object_or_None(Products,barcode = logging_object[key]["barcode"])
                    logging_object[key]["balance_after"] = user.kiosk_balance
                    logging_object[key]["stock_after_change"] = product.amount

                #Log everything
                KioskView.log_object(logging_object) 
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
                        id = KioskView.register_product(barcode)
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
                        id = KioskView.register_user(rfid)
                        return HttpResponse(id)
                    else:
                        return HttpResponse(f"{rfid}, {user.given_name} {user.family_name}, {user.kiosk_balance}")

            else:
                return HttpResponse("-1") # Bad request

    
    @staticmethod
    def user_balance(rfid, balance_change:int):
        user = RFIDUser.object.get(rfid = rfid)
        if user.kiosk_balance + balance_change > 0:
            #balance change is negative if we subtract and positive if we add
            user.kiosk_balance += balance_change
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
                RFIDUser.object.create(given_name=random_id, family_name="",phone_mnumber="",email="", rfid=rfid, kiosk_balance=0) #create user in database with id
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
                data[key]["balance_after"], data[key]["balance_before"],
                data[key]["stock_before_change"], data[key]["stock_after_change"],
            )
   
            
