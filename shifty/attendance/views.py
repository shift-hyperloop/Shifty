import os
import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from slack import WebClient

from .models import Attendance, AtOffice
from .models import RFIDUser
from .forms import RegisterForm

class RFIDView:
    """
    Endpoint for posting RFID info
    """

    @staticmethod
    @csrf_exempt
    def rfid_endpoint(request):
        if request.method == 'POST':
            rfid = request.POST['rfid']

            try:
                print(rfid)
                user = RFIDUser.objects.get(rfid=rfid)
            except Exception as e:
                user = None

            if user:

                current_time = datetime.datetime.now()

                attendance = Attendance.objects.filter(user=user).order_by('-check_in').first()
                at_office_obj = AtOffice.objects.all().first()
                

                if not attendance:
                    Attendance.objects.create(user=user, check_in=current_time)
                    at_office_num = at_office_obj.at_office
                    if at_office_num == 0:
                        RFIDView.office_opened()
                    at_office_num += 1
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()

                elif attendance.check_out:
                    Attendance.objects.create(user=user, check_in=current_time)
                    at_office_num = at_office_obj.at_office
                    if at_office_num == 0:
                        RFIDView.office_opened()
                    at_office_num += 1
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()
                else:
                    at_office_num = at_office_obj.at_office
                    if at_office_num == 1:
                        RFIDView.office_closed()
                    at_office_num -= 1
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()
                    setattr(attendance, 'check_out', current_time)
                    attendance.save()

                return JsonResponse(dict(success=True))
            else:
                print('User not registered!')

    @staticmethod
    def office_opened():
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)
        client.chat_postMessage(channel='#office-status', text='Office is OPEN!')

    @staticmethod
    def office_closed():
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)
        client.chat_postMessage(channel='#office-status', text='Office is CLOSED!')


