from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.http import JsonResponse

class Doorbell:

    def __init__(self):
        self.is_ringing = False

    @csrf_exempt
    def doorbell(self, request):
        if request.method == 'POST':
            self.is_ringing = True
            return HttpResponse(200)

        elif request.method == 'GET':
            return JsonResponse({'is_ringing': self.is_ringing})

        
