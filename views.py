from urllib import response
import uuid
from django.contrib.auth import logout as logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm,StorageForm,LoginForm,CollectionForm,GetOtpForm,PaymentForm,MobileForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from django_daraja.mpesa.core import MpesaClient
from .models import Storage,Otp,Payment
#from .utils import generate_otp, send_otp_via_email  
import random



@login_required(login_url='login')
def home(request):
    storages = Storage.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Storage.objects.filter(id=post_id).first()
            if post and (Storage.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = Storage.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'main/home.html', {"storages": storages})


@login_required(login_url="/login")
def store(request):
    if request.method == 'POST':
        form = StorageForm(request.POST)
        if form.is_valid():
              form.save()
              e_mail = form.cleaned_data['email']
              customer = User.objects.get(email=e_mail)
              email = customer.email
              name = customer.username
              if email is not None:
                   subject = f'Hey {name},'
                   message = 'We are happy for you have stored with us. Be comfortable because your luggage is safe with us. Collect it when you are done with your errands.'
                   from_email = 'hianilstorages@gmail.com'
                   recipient_list = [
                                  email
                                 ]
                   send_mail(
                         subject,
                         message,
                         from_email,
                         recipient_list,
                         fail_silently=False,
                        )
                   return redirect('/home')
              else:
                   return HttpResponse("Use the email address you used to sign up")
        else:
            form.add_error(None, 'Fill the form correctly')

    else:
        form = StorageForm()

    return render(request, 'main/store.html', {"form": form})
    
    
@login_required(login_url="/login")
def collect(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            e_mail = form.cleaned_data['email']
            storage = Storage.objects.get(id_number=id_number)
            customer = User.objects.get(email=e_mail)
            email = customer.email
            name = customer.username
            stored_at = storage.stored_at
            current_time = timezone.now() 
            time_taken = current_time - stored_at
            fee = (time_taken.total_seconds() /3600)*100
            subject = f'Collect your Luggage {name},'
            message = f'{name}, We are very happy to see you come back to collect your Luggage. \n\n pay ksh {fee} to get the passcode to unlock the safe and collect your bag'  
            from_email = 'hianilstorages@gmail.com'
            recipient_list = [
                                email
                             ]
            
            send_mail(
                         subject,
                         message,
                         from_email,
                         recipient_list,
                         fail_silently=False,
                        )
            return redirect('/add_payment_number')
        else:
            form.add_error(None, 'ID not found')

    else:
        form = CollectionForm()

    return render(request, 'main/collect.html', {"form": form})

        

def generate_otp():
    return str(random.randint(100000, 999999))

     
@login_required
def get_otp(request):
    if request.method == 'POST':
        form = GetOtpForm(request.POST)
        if form.is_valid():
            safe_number = form.cleaned_data['safe_number']
            #email = form.cleaned_data['email']
            user = Storage.objects.get(safe_number=safe_number )
            email = user.email
            otp = generate_otp()
            Otp.objects.otp = otp
            subject = 'Your Safe Password'
            message = f'Your Password is {otp}. Please use this to unlock the safe and pick your bag.\n Note that the password will expire after 5 minutes.\n'
            email_from = 'hianilstorages@gmail.com'
            recipient_list = [
                                email
                            ]
            send_mail(subject, message, email_from, recipient_list,fail_silently=False,)
            #return  messages.success (request, 'password has been sent to your email.')
            return redirect ('/home')
        else:
            messages.error(request, 'Safe not found.')
    else:
        form = GetOtpForm()
        return render(request, 'main/get_otp.html', {"form":form})
    
    
                
            
               
               
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})



def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username,password=password)  
           if user is not None:
                login(request,user)
                return redirect('/home')
        else:
               messages.error(request, 'Invalid username or password')
               return HttpResponse("Try again. <a href='/home'>Go to home page</a>")
    else:
       
        form = LoginForm() 
        return render(request, 'registration/login.html', {'form': form})
    
    
    
    
    


def logout(request):
    if request.method == 'POST':
      logout(request)
      return redirect('/login')
  
def add_payment_number(request):
    if request.method == 'POST':
        form = MobileForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect('/payment')
        else:
             messages.error(request, 'Enter phone number')
    else:
        form = MobileForm()
        
    return render(request, 'main/add_payment_number.html', {"form": form})

def generate_transaction_code():
        return uuid.uuid4().hex[:12].upper()
            

def payment(request):
 cl = MpesaClient()
 if request.method == 'POST':
      form = PaymentForm(request.POST)
      if form.is_valid():
          mobile_number = form.cleaned_data['mobile_number']
          safe_number = form.cleaned_data['safe_number']
          payment = Payment.objects.get(mobile_number= mobile_number)
          storage = Storage.objects.get(safe_number=safe_number)
          otp = generate_transaction_code()
          payment.transaction_code = otp
          stored_at = storage.stored_at
          number = payment.mobile_number
          current_time = timezone.now() 
          time_taken = current_time - stored_at
          fee = (time_taken.total_seconds() /3600) * 100
          payment.amount = int(fee)
           # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
          phone_number = f'{number}'
          amount = payment.amount
          account_reference = 'Hianilstorages'
          transaction_desc = 'Pay to collect your luggage '
          callback_url = 'https://2390-102-219-210-90.ngrok-free.app/express-app'
          response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
          return redirect('/otp')
      else:
           messages.error(request, 'Enter phone number')
 else:
    form = PaymentForm()
 return render(request, 'main/payment.html',{'form':form})
    
        

def stk_push_callback(request):
        data = request.body
        
        return redirect('/otp')