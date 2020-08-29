from django import forms

from .models import RFIDUser

class RegisterForm(forms.ModelForm):

    given_name = forms.CharField(max_length=50)
    family_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    class Meta:
        """
        Meta class
        """
        model = RFIDUser
        fields = ['given_name', 'family_name', 'email']


 
