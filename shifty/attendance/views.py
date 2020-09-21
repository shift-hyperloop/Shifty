import os
import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
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
    @csrf_exempt 
    def checkin(request):
        """
        Function for checking in
        :param request: The http request
        :return: The rendered HTML file
        """
        if request.method == 'GET':
            return render(request, 'attendance/checkin.html')
        

    @staticmethod
    @csrf_exempt 
    def success(request):
        return render(request, 'attendance/checkin_success.html')


class CheckoutView:
    """
    Class for the check-out view
    """

    @staticmethod
    @csrf_exempt 
    def checkout(request):
        """
        Function for checking out
        :param request: The http request
        :return: The rendered HTML file
        """
        if request.method == 'GET':
            return render(request, 'attendance/checkout.html')
        

    @staticmethod
    @csrf_exempt 
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
        if request.method == 'GET':
            form = RegisterForm()

            return render(request, 'attendance/register.html', {'form': form})

        elif request.method == 'POST':
            form = RegisterForm(request.POST)

            # Save model from form is valid
            if form.is_valid():
                user = form.save()
                user.save()
                
                given_name = getattr(user, 'given_name')
                family_name = getattr(user, 'family_name')
                message = f'{given_name} {family_name}'  
                request.user.message_set.create(message=message) 
                return redirect('/rfid_register')

    @staticmethod
    def success(request):
        """
        Function for displaying registration success
        :param request: The http request
        :return: The rendered HTML file
        """
        return render(request, 'attendance/registration_success.html')

    @staticmethod
    def rifd_register(request):
        return render(request, 'attendance/rfid_register.html')

class RFIDView:
    """
    Endpoint for posting RFID info
    """

    
    @csrf_exempt
    def rfid_endpoint(request):
        if request.method == 'POST':
            rfid = request.POST['rfid']

            try:
                user = RFIDUser.objects.get(rfid=rfid)
            except Exception as e:
                user = None

            if user:

                current_time = datetime.datetime.now()

                attendance = Attendance.objects.all().order_by('-check_in').first()

                if not attendance:
                    Attendance.objects.create(user=user, check_in=current_time)
                elif attendance.check_out:
                    Attendance.objects.create(user=user, check_in=current_time)
                else:
                    setattr(attendance, 'check_out', current_time)
                    attendace.save()

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


