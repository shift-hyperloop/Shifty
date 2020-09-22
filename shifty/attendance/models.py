from django.db import models

class Attendance(models.Model):
    """
    Class for Attendance model
    """
    user = models.ForeignKey('RFIDUser', on_delete=models.CASCADE,
                             related_name='rfid_user', default=None,
                             blank=True, null=True)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)

class RFIDUser(models.Model):
    """
    Class for RFIDUser model
    """
    given_name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    rfid = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.given_name} {self.family_name}'

class AtOffice(models.Model):
    """
    Class for AtOffice model
    """
    at_office = models.IntegerField()


