from django.contrib import admin

from .models import RFIDUser, Attendance, AtOffice

admin.site.register(RFIDUser)
admin.site.register(Attendance)
admin.site.register(AtOffice)
