import datetime

from django.shortcuts import render, redirect

from rfid.rfid_interface import RFIDInterface
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
        rfid_interface = RFIDInterface()
        rfid = rfid_interface.read()

        user = RFIDUser.objects.get(rfid = rfid)

        time = datetime.datetime.now()

        Attendance.objects.create(user=user, check_in=time)

        return render(request, 'attendance/checkin_success.html')

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
        rfid_interface = RFIDInterface()
        rfid = rfid_interface.read()

        if request.method == 'POST':

            form = RegisterForm(request.POST, request.FILES)
            form.rfid = rfid

            # Save model from form is valid
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.save()
                return redirect('/registration_success')
            else:
                print(form.errors)
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
