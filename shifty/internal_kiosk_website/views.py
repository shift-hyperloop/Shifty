from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from internal_kiosk_website.models import Products
from django.test import Client

@login_required
def index(request):
    csrf_client = Client(enforce_csrf_checks=True)
    if request.method == "POST":
        data = dict(request.POST)
        if "csrfmiddlewaretoken" in data.keys():
            csrf_token = data.pop("csrfmiddlewaretoken",None)

            for key in data.keys():
                for i,d in enumerate(data[key]):
                    try:
                        data[key][i]=int(d)
                    except:
                        data[key][i]=0
                print(data)

    prods = Products.objects.all()     

    context = {
        'prods': prods,
    }
    return render(request,'index.html',context)

