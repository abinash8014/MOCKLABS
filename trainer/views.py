from django.shortcuts import render
from manager.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from trainer.forms import *
from student.models import *
import random
from django.core.mail import send_mail

# Create your views here.
def trainer_login_required(func):
    def inner(request,*args,**kwargs):
        tun = request.session.get('trainerun')
        if tun:
            return func(request,*args,**kwargs)
        return HttpResponseRedirect(reverse('trainer_login'))
    return inner

def trainer_home(request):
    return render(request,'trainer/trainer_home.html')

def trainer_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un,password=pw)
        if AUO and AUO.is_active:
            EP = EmployeeProfile.objects.get(username=AUO)
            if AUO.is_staff and EP.Role == 'Trainer':
                login(request,AUO)
                request.session['trainerun'] = un
                return HttpResponseRedirect(reverse('trainer_home'))
            return HttpResponse('This is not a Trainer creds')
        return HttpResponse('Invalid Credentials')
    return render(request,'trainer/trainer_login.html')

@trainer_login_required
def trainer_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('trainer_home'))

@trainer_login_required
def start_mock(request):
    ERFO = RatingForm()
    std_prf = StudentProfile.objects.all()
    d = {'ERFO':ERFO,'std_prf':std_prf}
    if request.method == 'POST':
        RFDO = RatingForm(request.POST)
        SDO = request.POST.get('student')
        if RFDO.is_valid():
            tun = request.session.get('trainerun')
            TO = User.objects.get(username=tun)
            MRFDO = RFDO.save(commit=False)
            MRFDO.conducted_by = TO
            
            # get the student object
            SO = User.objects.get(username=SDO)
            MRFDO.student = SO
            MRFDO.save()
            return HttpResponseRedirect(reverse('start_mock'))
        return HttpResponse('Invalid Data')
    return render(request,'trainer/start_mock.html',d)

def trainer_forget_pw(request):
    if request.method == "POST":
        un = request.POST.get('un')
        # UO = User.objects.filter(username=un, is_staff=True, is_superuser=False).first()  # Ensuring only Trainers
        UO = User.objects.get(username=un)
        EO = EmployeeProfile.objects.get(username=UO)
        print(EO)
        if UO and UO.is_active and UO.is_staff and EO.Role=='Trainer':
            otp = random.randint(1000,9999)
            print(otp)
            #email = UO.email
            #print(email)
            # send_mail(
            #     'Forget your pw?',
            #     'Here is your OTP:{otp}'
            #     'abinashsahoo063@gmail.com',
            #     [email],
            #     fail_silently=False
            # )
            request.session['trainerotp'] = otp
            request.session['trainerun'] = un
            return HttpResponseRedirect(reverse('trainer_otp'))
        
        return HttpResponse('User not found or not a Trainer')
    
    return render(request,'trainer/trainer_forget_pw.html')

def trainer_otp(request):
    if request.method == 'POST':
        eotp=request.POST.get('otp')
        gotp=request.session.get('trainerotp')
        un = request.session.get('trainerun')
        if int(eotp)==gotp:
            UO = User.objects.get(username=un)
            login(request,UO)
            return HttpResponseRedirect(reverse('trainer_change_pw'))
        return HttpResponse('Otp not Matched')
    return render(request,'trainer/trainer_otp.html')

def trainer_change_pw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            username = request.session.get('trainerun')
            UO = User.objects.get(username=username)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('trainer_login'))
        return HttpResponse('password Not Matched')
    return render(request,'trainer/trainer_change_pw.html')