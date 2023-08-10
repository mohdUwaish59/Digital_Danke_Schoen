from django import forms
from .models import EmailSubscriber

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    country_code = forms.CharField(max_length=5)

class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscriber
        fields = ['email']   

class ForgetPasswordForm(forms.ModelForm):
    class Meta:
        fields = ['email']  