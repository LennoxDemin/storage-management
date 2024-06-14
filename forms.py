from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Storage,Payment,Otp



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1"]
        
class LoginForm(AuthenticationForm):
    
    class Meta:
         model = User
         fields = ["username", "password"]
         
         

class StorageForm(forms.ModelForm):
    
    class Meta:
        model = Storage
        fields = ["first_name", "last_name","email","id_number","safe_number","luggage_weight_in_kgs", "luggage_description"]
        
class CollectionForm(forms.ModelForm):
    
    class Meta:
        model = Storage
        fields = ["email","id_number"]
        
        
class GetOtpForm(forms.ModelForm):
    
    class Meta:
        model = Storage
        fields = ["safe_number"]
        
        
class MobileForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        fields = ["mobile_number"]
        
        
class PaymentForm(forms.Form):
    
    mobile_number = forms.CharField(max_length=15)
    safe_number = forms.IntegerField()
