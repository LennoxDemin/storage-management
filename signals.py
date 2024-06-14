from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone


@receiver(post_save)
def create_token(sender,email,created,**kwargs):
    if created:
        if email is not None:
          OtpToken.objects.create( user=email ,otp_expired_at=timezone.now() + timezone.timedelta(minutess=5))
          email.save()
        else:
            
          otp=OtpToken.objects.filter(user=email).last()
    
    subject="Email Verification"
    message = f"""
                                Hi {email.username}, The payment has been received successifuly.\n Here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use it to unlock the safe and secure your luggage. \n\n THANK YOU FOR TRUSTING IN US AND WELCOME AGAIN
                                
                                """
    sender = "hianilstorages@gmail.com"
    receiver = [email.email, ]
         # send email
    send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
        