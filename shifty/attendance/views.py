import os
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from slack import WebClient

from .models import Attendance, AtOffice
from .models import RFIDUser

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
                    RFIDView.update_at_office(at_office_num)
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()
                    return JsonResponse(dict(success=True, type='check_in'))

                elif attendance.check_out:
                    Attendance.objects.create(user=user, check_in=current_time)
                    at_office_num = at_office_obj.at_office
                    if at_office_num == 0:
                        RFIDView.office_opened()
                    at_office_num += 1
                    RFIDView.update_at_office(at_office_num)
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()
                    return JsonResponse(dict(success=True, type='check_in'))

                else:
                    at_office_num = at_office_obj.at_office
                    if at_office_num == 1:
                        RFIDView.office_closed()
                    at_office_num -= 1
                    RFIDView.update_at_office(at_office_num)
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()
                    setattr(attendance, 'check_out', current_time)
                    attendance.save()

                    return JsonResponse(dict(success=True, type='check_out'))
            else:
                return JsonResponse(dict(success=False))

    @staticmethod
    def office_opened():
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)
        client.chat_update(channel='C01BV9EHN48', ts='1601053648.000100', text='Office is OPEN! :green_apple:')

    @staticmethod
    def office_closed():
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)
        client.chat_update(channel='C01BV9EHN48', ts='1601053648.000100', text='Office is CLOSED! :red_circle:')
    
    @staticmethod
    def update_at_office(at_office: int):
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)
        client.chat_update(channel='C01BV9EHN48', ts='1601054690.000600', text=f'Currently at office: {at_office}')
