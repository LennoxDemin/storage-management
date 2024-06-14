from django.urls import path
from . import views


urlpatterns = [
    path('',views.home),
    path('home',views.home,name='home'),
    path('sign-up',views.sign_up, name='sign-up'),
    #path('accounts/login/?next=',views.sign_in, name='login'),
    path('login',views.sign_in, name='login'),
    path('store',views.store, name='store'),
    path('collect',views.collect, name='collect'),
    path('otp',views.get_otp),
    path('add_payment_number', views.add_payment_number, name='add_payment_number'),
    path('payment', views.payment, name='payment'),
    path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),

    path('logout',views.logout),
    
]
