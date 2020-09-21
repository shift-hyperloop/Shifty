from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.http import JsonResponse
from .models import Ringing


@csrf_exempt
def doorbell(request):
    if request.method == 'POST':
        set_ringing(True)
        return HttpResponse(200)

    elif request.method == 'GET':
        ringing = get_ringing()
        set_ringing(False)
        return JsonResponse({'is_ringing': ringing})

def set_ringing(value: bool):
    ringing = Ringing.objects.all()
    if ringing.count() == 0:
        ringing.create(is_ringing=value)
    else:
        current_ringing = ringing.first()
        setattr(current_ringing, 'is_ringing', value)
        current_ringing.save()

def get_ringing():
    return Ringing.objects.first().is_ringing

        
