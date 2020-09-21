from django.db import models

class Ringing(models.Model):
    """
    Class for Attendance model
    """
    is_ringing = models.BooleanField(unique=True)