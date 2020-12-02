from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from internal_kiosk_website.models import Products
from django.test import Client
import re

@login_required
def index(request):
    csrf_client = Client(enforce_csrf_checks=True)
    if request.method == "POST":
        data = dict(request.POST)
        if "csrfmiddlewaretoken" in data.keys():
            csrf_token = data.pop("csrfmiddlewaretoken",None)
            for key in list(data.keys())[::-1]: #Change the name last
                if '' not in data[key]:
                    if len(re.findall("[^A-Za-z0-9- ]", data[key][0])) == 0:
                        name = key.split("_")[0]
                        item = Products.object.get(name = name)
                        if "_name" in key:
                            item.name = data[key][0]
                            item.save()
                        elif "_price" in key:
                            item.price = int(data[key][0])
                            item.save()
                        elif "_stock" in key:
                            item.amount += int(data[key][0])
                            item.save()
                    else:
                        print("weird character found")

    prods = Products.object.all() 

    context = {
        'prods': prods,
    }
    return render(request,'index.html',context)

