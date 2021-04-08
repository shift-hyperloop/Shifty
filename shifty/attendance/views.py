import sys
import os
print (os.getcwd())
sys.path.append("..")
sys.path.append(".")

import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from slack import WebClient
from slack.errors import SlackApiError

from .models import Attendance, AtOffice
from .models import RFIDUser

from utils.logger import create_logger

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
                print(f"rfid: {rfid}")
                user = RFIDUser.objects.get(rfid=rfid)
                print("user found")
            except Exception as e:
                user = None
                print("found = none")
            if user:

                current_time = datetime.datetime.now()

                attendance = Attendance.objects.filter(user=user).order_by('-check_in').first()
                at_office_obj = AtOffice.objects.all().first()
                print(attendance)

                if not attendance:
                    Attendance.objects.create(user=user, check_in=current_time)
                    at_office_num = at_office_obj.at_office
                    at_office_num += 1
                    RFIDView.update_at_office(at_office_num)
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()
                    return JsonResponse(dict(success=True, type='check_in'))

                elif attendance.check_out:
                    Attendance.objects.create(user=user, check_in=current_time)
                    at_office_num = at_office_obj.at_office
                    at_office_num += 1
                    RFIDView.update_at_office(at_office_num)
                    setattr(at_office_obj, 'at_office', at_office_num) 
                    at_office_obj.save()
                    return JsonResponse(dict(success=True, type='check_in'))

                else:
                    at_office_num = at_office_obj.at_office
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
    def _delete_messages():
        logger = create_logger()
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)

        conversation_history = []
        channel_id = "C01BV9EHN48"

        try:
            # Get all messages and delete, should only be 2 messages for Office Status channel
            
            result = client.conversations_history(channel=channel_id)
            conversation_history = result["messages"]

            for message in conversation_history:
                m_ts = message["ts"]
                client.chat_delete(channel=channel_id, ts=m_ts)

        except SlackApiError as e:
            logger.debug("Error deleting conversation history: {}".format(e))

    
    @staticmethod
    def update_at_office(at_office: int):
        logger = create_logger()
        RFIDView._delete_messages()
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)
        channel_id = "C01BV9EHN48"

        try:
            if at_office > 0:
                client.chat_postMessage(channel=channel_id, text=f'Office is OPEN! :green_apple: Currently at office: {at_office}')
            else:
                client.chat_postMessage(channel=channel_id, text=f'Office is CLOSED!')
        except SlackApiError as e:
            logger.debug("Error posting message: {}".format(e))



