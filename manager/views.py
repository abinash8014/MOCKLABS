from django.shortcuts import render
from manager.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import random
import string
from  django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# def login_required(func):
#    def inner(request,*args,**kwargs):
#        un = request.session.get('username')
#        if un:
#            return func(request,*args,**kwargs)
#        return HttpResponseRedirect(reverse('manager_login')) 
#    return inner

def manager_home(request):
    return render(request,'manager/manager_home.html')

@login_required
def add_employee(request):
    EEUFO = EmployeeUserForm()
    EEPFO = EmployeeProfileForm()
    d = {'EEUFO':EEUFO,'EEPFO':EEPFO}
    if request.method == 'POST':
        EUFDO = EmployeeUserForm(request.POST)
        EPFDO = EmployeeProfileForm(request.POST)
        if EUFDO.is_valid() and EPFDO.is_valid():
            un = f"{EUFDO.cleaned_data.get('first_name')}{EPFDO.cleaned_data.get('pno')[-4:]}"
            pw = ''.join([random.choice(string.digits) for i in range(1,6)])
            email = EUFDO.cleaned_data.get('email')
            MEUFDO = EUFDO.save(commit=False)
            MEUFDO.username = un
            MEUFDO.set_password(pw)
            MEUFDO.is_staff = True
            MEUFDO.save()
            
            MEPFDO = EPFDO.save(commit=False)
            MEPFDO.username = MEUFDO
            MEPFDO.save()
            message = f"""Hello,Here are your account details:
            Username: {un}
            Password: {pw}
            Please keep this information secure and rememer it.
            And Don't Share this to anyone.

            Best Regards,
            QSPIDER/PYSPIDER/JSPIDER"""
            
            send_mail(
                'Sucessfully Added New Employee',
                message,
                'abinashsahoo063@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('manager_home'))
        return HttpResponse('Invalid Data')
    return render(request,'manager/add_employee.html',d)

def manager_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un,password=pw)
        if AUO and AUO.is_active and AUO.is_staff:
            if AUO.is_superuser:
                login(request,AUO)
                request.session['managerun'] = un
                return HttpResponseRedirect(reverse('manager_home'))
            return HttpResponse('Not a admin.')
        return HttpResponse('Invalid Credentials.')
    return render(request,'manager/manager_login.html')

@login_required
def manager_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('manager_home'))

def manager_forget_pw(request):
    if request.method == "POST":
        un = request.POST.get('un')
        UO = User.objects.filter(username=un, is_superuser=True).first()  # Ensuring only Managers
        
        if UO:
            otp = random.randint(1000,9999)
            print(otp)
            request.session['managerotp'] = otp
            request.session['managerun'] = un
            return HttpResponseRedirect(reverse('manager_otp'))
        
        return HttpResponse('User not found or not a Manager')
    
    return render(request,'manager/manager_forget_pw.html')


def manager_otp(request):
    if request.method == 'POST':
        eotp=request.POST.get('otp')
        gotp=request.session.get('managerotp')
        un = request.session.get('managerun')
        if int(eotp)==gotp:
            UO = User.objects.get(username=un)
            login(request,UO)
            return HttpResponseRedirect(reverse('manager_change_pw'))
        return HttpResponse('Otp not Matched')
    return render(request,'manager/manager_otp.html')

def manager_change_pw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            username = request.session.get('managerun')
            UO = User.objects.get(username=username)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('manager_login'))
        return HttpResponse('password Not Matched')
    return render(request,'manager/manager_change_pw.html')
