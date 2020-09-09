import os
import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from slack import WebClient

from .models import Attendance
from .models import RFIDUser
from .forms import RegisterForm


class CheckinView:
    """
    Class for the check-in view
    """

    @staticmethod
    def checkin(request):
        """
        Function for checking in
        :param request: The http request
        :return: The rendered HTML file
        """
        if request.method == 'GET':
            return render(request, 'attendance/checkin.html')
        

    @staticmethod
    def success(request):
        return render(request, 'attendance/checkin_success.html')


class CheckoutView:
    """
    Class for the check-out view
    """

    @staticmethod
    def checkout(request):
        """
        Function for checking out
        :param request: The http request
        :return: The rendered HTML file
        """
        if request.method == 'GET':
            return render(request, 'attendance/checkout.html')
        

    @staticmethod
    def success(request):
        return render(request, 'attendance/checkout_success.html')

        

class RegisterView:
    """
    Class for the register view
    """

    @staticmethod
    def register(request):
        """
        Function for registration
        :param request: The http request
        :return: The rendered HTML file
        """
        if request.method != 'POST':
            form = RegisterForm()

        return render(request, 'attendance/register.html', {'form': form})

    @staticmethod
    def success(request):
        """
        Function for displaying registration success
        :param request: The http request
        :return: The rendered HTML file
        """
        return render(request, 'attendance/registration_success.html')

class RFIDView:
    """
    Endpoint for posting RFID info
    """

    def __init__(self):
        self.at_office = 0
        self.slack_api_token = os.environ.get('SLACK_API_TOKEN')

    @csrf_exempt 
    def rfid_endpoint(self, request):
        if request.method == 'POST':
            rfid = request['rfid']
            request_type = request['type']

            if request_type == 'checkin':
                try:
                    user = RFIDUser.objects.get(rfid=rfid)
                except RFIDUser.DoesNotExist:
                    return False

                checkin_time = datetime.datetime.now()

                Attendance.objects.create(user=user, check_in=checkin_time)
                if self.at_office == 0:
                    self.office_opened()

                self.at_office += 1
                return redirect('/checkin_success')

            elif request_type == 'checkout':
                try:
                    user = RFIDUser.objects.get(rfid=rfid)
                except RFIDUser.DoesNotExist:
                    return False

                checkout_time = datetime.datetime.now()

                attendace = Attendance.objects.filter(user=user).order_by('-check_in').first()
                setattr(attendace, 'check_out', checkout_time)
                attendace.save()

                self.at_office -= 1
                if self.at_office == 0:
                    self.office_closed()

                return redirect('/checkout_success')

            elif request.type == 'register':
                form = RegisterForm(request.POST)

                # Save model from form is valid
                if form.is_valid():
                    user = form.save()
                    setattr(user, 'rfid', rfid)
                    user.save()
                    return redirect('/registration_success')

    def office_opened(self):
        client = WebClient(token=self.slack_api_token)
        client.chat_postMessage(channel='#office-status', text='Office is OPEN!')


    def office_closed(self):
        client = WebClient(token=self.slack_api_token)
        client.chat_postMessage(channel='#office-status', text='Office is CLOSED!')


