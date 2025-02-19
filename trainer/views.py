from django.shortcuts import render
from manager.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
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

def trainer_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('trainer_home'))