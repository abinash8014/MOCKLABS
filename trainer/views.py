from django.shortcuts import render
from manager.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from trainer.forms import *
from student.models import *

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