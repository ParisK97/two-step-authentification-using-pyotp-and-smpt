from django.shortcuts import render, redirect
import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .forms import UserInfoForm
from django.contrib import messages
import os
from dotenv import load_dotenv
# Create your views here.

load_dotenv()
# generate opt
def generate_otp()->str:
    key = pyotp.random_base32()
    hotp = pyotp.HOTP(key)

    counter = 1
    otp = hotp.at(counter)

    return otp

def send_mail(recipient:str, first_name:str, otp:str) ->None:
    sender = os.getenv('EMAIL_HOST_USER')
    PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    subject = 'Complete Your Signup with This OTP'

    with open('static/text/registration_text.txt', 'r') as file:
        content = file.read()
    
    body= content.format(name=first_name, otp=otp)  
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    HOST_EMAIL = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    combine = f'{HOST_EMAIL}:{EMAIL_PORT}'

    with smtplib.SMTP(combine) as server:
        server.starttls()  
        server.login(sender, PASSWORD)  
        server.send_message(msg)

def user_registration(request):
    page = 'registration'
    global otp
    otp = generate_otp() # generate otp
    
    if request.method == 'POST':
        recipient = request.POST.get('email')
        first_name = request.POST.get('first_name')

        global registration_form
        registration_form = UserInfoForm(request.POST)

        if registration_form.is_valid():
            registration_form.save(commit=False)
            send_mail(recipient, first_name, otp) # send mail
            return redirect('activate-account')
        else:
            messages.error(request, 'An error occured during registration')
    else:
        registration_form = UserInfoForm()

    context = {'registration_form': registration_form, 'page': page}
    return render(request, 'accounts/registration.html', context)

def activate_account(request):
    if request.method == 'POST':
        if request.POST.get('verify-otp') == otp:
            registration_form.save()
            print(messages.success(request, 'Account successfully activated'))
        else:
            print(messages.error(request, 'Invalid OTP'))
    return render(request, 'accounts/registration.html')

