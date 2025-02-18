from django.shortcuts import render
from manager.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import random
import string
from  django.core.mail import send_mail
# Create your views here.

def manager_home(request):
    return render(request,'manager/manager_home.html')

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
            MEUFDO = EUFDO.save(commit=False)
            MEUFDO.username = un
            MEUFDO.set_password(pw)
            email = EUFDO.cleaned_data.get('email')
            MEUFDO.is_staff = True
            MEUFDO.save()
            MEPFDO = EPFDO.save(commit=False)
            MEPFDO.username = MEUFDO
            MEPFDO.save()
            message = f"""Hello,Here are your account details:
            Username: {un}
            Password: {pw}
            Please keep this information secure.

            Best Regards,
            QSPIDER/PYSPIDER/JSPIDER"""
            
            send_mail(
                'Sucessfully Added New Employee',
                message,
                'abinashsahoo063@gmail.com',
                [email],
                fail_silently=False
            )
            request.session['username'] = un
            request.session['password'] = pw
            return HttpResponseRedirect(reverse('manager_home'))
        return HttpResponse('Invalid Data')
    return render(request,'manager/add_employee.html',d)

