from django.shortcuts import render
from manager.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from hr.models import  *

# Create your views here.

def hr_login_required(func):
    def inner(request,*args,**kwargs):
        hrun = request.session.get('hrun')
        if hrun:
            return func(request,*args,**kwargs)
        return HttpResponseRedirect(reverse('hr_login'))
    return inner

def hr_home(request):
    return render(request,'hr/hr_home.html')

def hr_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un,password=pw)
        if AUO and AUO.is_active:
            emp_profile = EmployeeProfile.objects.get(username=AUO)
            if AUO.is_staff and emp_profile.Role == 'HR':
                login(request,AUO)
                request.session['hrun'] = un
                return HttpResponseRedirect(reverse('hr_home'))
            return HttpResponse('This is not a hr')
        return HttpResponse('Invalid Credentials')
    return render(request,'hr/hr_login.html')

@hr_login_required
def hr_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('hr_home'))

@hr_login_required
def mock_ratings(request):
    SO = StudentRating.objects.all()
    d = {'SO':SO}
    return render(request,'hr/mock_ratings.html',d)
