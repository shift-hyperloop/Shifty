from django.db import models

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

