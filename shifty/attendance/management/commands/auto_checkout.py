import datetime
import os

from slack import WebClient

from django.core.management.base import BaseCommand, CommandError
from attendance.models import Attendance, AtOffice
from attendance.views import RFIDView

class Command(BaseCommand):
    help = 'Automatically checks out people from the office'

    def handle(self, *args, **options):
        attendances = Attendance.objects.filter(check_out=None)
        current_time = datetime.datetime.now()
        for a in attendances:
            self.send_notification(a)
            setattr(a, 'check_out', current_time)
            a.save()

        at_office = AtOffice.objects.first()
        setattr(at_office, 'at_office', 0)
        at_office.save()

        RFIDView.update_at_office(0)
        RFIDView.office_closed()

        Attendance.objects.filter(check_in__lte=datetime.datetime.now() - datetime.timedelta(days=10)).delete()

    def send_notification(self, attendance: Attendance):
        slack_api_token = os.environ.get('SLACK_API_TOKEN')
        client = WebClient(token=slack_api_token)

        for user in client.users_list()['members']:
            profile = user['profile']
            keys = profile.keys()
            if 'first_name' in keys and 'last_name' in keys:
                if profile['first_name'] == attendance.user.given_name and profile['last_name'] == attendance.user.family_name:
                    user_id = user['id']
                    client.chat_postMessage(channel=user_id, as_user=True, text=':red_circle: You forgot to check out of the office during your last visit!')

        
