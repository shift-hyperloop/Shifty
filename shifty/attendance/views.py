import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        if request.method == 'POST':
            
            data = {
                'success': CheckinView.post_attendance()
            }
            return JsonResponse(data)

        elif request.method == 'GET':
            return render(request, 'attendance/checkin.html')
        

    @staticmethod
    def success(request):
        return render(request, 'attendance/checkin_success.html')

    @staticmethod
    def post_attendance() -> bool:
        rfid_interface = RFIDInterface()
        rfid = rfid_interface.read()

        try:
            user = RFIDUser.objects.get(rfid=rfid)
        except RFIDUser.DoesNotExist:
            return False

        checkin_time = datetime.datetime.now()

        Attendance.objects.create(user=user, check_in=checkin_time)
        return True

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
        if request.method == 'POST':
            
            data = {
                'success': CheckoutView.post_attendance()
            }
            return JsonResponse(data)

        elif request.method == 'GET':
            return render(request, 'attendance/checkout.html')
        

    @staticmethod
    def success(request):
        return render(request, 'attendance/checkout_success.html')

    @staticmethod
    def post_attendance() -> bool:

        try:
            user = RFIDUser.objects.get(rfid=rfid)
        except RFIDUser.DoesNotExist:
            return False

        checkout_time = datetime.datetime.now()

        attendace = Attendance.objects.filter(user=user).order_by('-check_in').first()
        setattr(attendace, 'check_out', checkout_time)
        attendace.save()
        return True

        

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
        

        if request.method == 'POST':

            rfid_interface = RFIDInterface()
            rfid = rfid_interface.read()
            form = RegisterForm(request.POST)

            # Save model from form is valid
            if form.is_valid():
                user = form.save()
                setattr(user, 'rfid', rfid)
                #user.refresh_from_db()
                user.save()
                return redirect('/registration_success')
        else:
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
