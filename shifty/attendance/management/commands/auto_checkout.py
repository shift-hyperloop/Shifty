import datetime

from django.core.management.base import BaseCommand, CommandError
from attendance.models import Attendance
from attendance.views import RFIDView

class Command(BaseCommand):
    help = 'Automatically checks out people from the office'

    def handle(self, *args, **options):
        attendances = Attendance.objects.filter(check_out=None)
        current_time = datetime.datetime.now()
        for a in attendances:
            setattr(a, 'check_out', current_time)
            
        RFIDView.update_at_office(0)
        RFIDView.office_closed()

        