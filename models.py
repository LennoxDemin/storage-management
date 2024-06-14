from django.db import models
from django.contrib.auth.models import User
import secrets
    
class Storage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.IntegerField()
    safe_number = models.IntegerField()
    email = models.EmailField()
    luggage_weight_in_kgs = models.IntegerField()
    luggage_description = models.TextField(max_length=1000)
    stored_at = models.DateTimeField(auto_now_add=True)
    #otp = models.CharField(max_length=6,default=secrets.token_hex(3))
    #otp_created_at  = models.DateTimeField(auto_now_add=True)
    #otp_expired_at= models.DateTimeField(blank=True,null=True)
    

    def __str__(self):
        return self.first_name + " " + self.last_name

class Otp(models.Model):
    otp = models.CharField(max_length=6,default=secrets.token_hex(3))
    otp_created_at  = models.DateTimeField(auto_now_add=True)
       
       
    def __str__(self):
        return self.otp

class Payment(models.Model):
    mobile_number = models.CharField(max_length=15)
    amount = models.CharField(default=0, max_length=200)
    transaction_code = models.CharField(max_length=12,editable=False)
    paid_at = models.DateTimeField(auto_now_add=True)
         
    def __str__(self):
        return self.mobile_number 
    


