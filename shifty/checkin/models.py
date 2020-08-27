from django.db import models

class Attendance(models.Model):
    """
    Class for Attendance model
    """
    user = models.ForeignKey('RFIDUser', on_delete=models.CASCADE,
                             related_name='rfid_user', default=None,
                             blank=True, null=True)
    check_in = models.DateTimeField(auto_now_add=True, null=True)
    check_out = models.DateTimeField(auto_now=True, null=True)

