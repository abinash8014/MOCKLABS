from django.shortcuts import render
from student.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
import random
from django.core.mail import send_mail
import csv

# Create your views here.

def login_required(functionn):
    def inner(request,*args, **kwargs):
        un = request.session.get('username')
        if un:
            return functionn(request,*args,**kwargs)
        return HttpResponseRedirect(reverse('student_login'))
    return inner

def student_home(request):
    un = request.session.get('username')
    if un:
        SUFO = User.objects.get(username=un)
        d = {'SUFO':SUFO}
        return render(request,'student/student_home.html',d)
    return render(request,'student/student_home.html')

def student_register(request):
    # ESUFO = StudentUserForm()
    # ESPFO = StudentProfileForm()
    # d = {'ESUFO':ESUFO,'ESPFO':ESPFO}
    # if request.method == 'POST' and request.FILES:
    #     SUFDO = StudentUserForm(request.POST)
    #     SPFDO = StudentProfileForm(request.POST,request.FILES)
    #     if SUFDO.is_valid() and SPFDO.is_valid():
    #         pw = SUFDO.cleaned_data.get('password')
    #         MSUFDO = SUFDO.save(commit=False)
    #         MSUFDO.set_password(pw)
    #         MSUFDO.save()
    #         MSPFDO = SPFDO.save(commit=False)
    #         MSPFDO.username = MSUFDOstudent_
    #         MSPFDO.save()
    #         return HttpResponseRedirect(reverse('student_login'))
    #     return HttpResponse('Invalid Data')
    
    # return render(request,'student/student_register.html',d)
    
    with open(r"C:\Users\Abinash Sahoo\OneDrive\Desktop\Book 1(Sheet1).csv",'r') as file:
        csv_reader = csv.reader(file)
        next(file)
        for i in (csv_reader):
            UO = User(first_name = i[1], last_name = i[2], email = i[4], username = i[1]+i[2])
            UO.set_password(i[1])
            UO.save()
            PO = StudentProfile(username=UO, pno = i[3], add = i[6], course = i[5])
            PO.save()
    return HttpResponseRedirect(reverse('Done'))
            

def student_login(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        pw = request.POST.get('password')
        AUO = authenticate(username=un,password=pw)
        if AUO:
            login(request,AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('student_home'))
        return HttpResponse('Invalid Creds')
    return render(request,'student/student_login.html')

def student_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('student_home'))

@login_required
def see_schedule(request):
    sun = request.session.get('username')
    SO = User.objects.get(username=sun)
    d = {'SO':SO}
    return render(request,'student/see_schedule.html',d)

def student_forget_pw(request):
    if request.method == "POST":
        un = request.POST.get('un')
        # UO = User.objects.filter(username=un, is_staff=False, is_superuser=False).first()  # Ensuring only Students
        UO = User.objects.get(username=un)
        
        if UO and UO.is_active:
            if UO.is_staff and UO.is_superuser:
                return HttpResponse('it is not a student credential')
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
            request.session['studentotp'] = otp
            request.session['studentun'] = un
            return HttpResponseRedirect(reverse('student_otp'))
        
        return HttpResponse('User not found or not a Student')
    
    return render(request,'student/student_forget_pw.html')


def student_otp(request):
    if request.method == 'POST':
        eotp=request.POST.get('otp')
        gotp=request.session.get('student_otp')
        un = request.session.get('studentun')
        if int(eotp)==gotp:
            UO = User.objects.get(username=un)
            login(request,UO)
            return HttpResponseRedirect(reverse('student_change_pw'))
        return HttpResponse('Otp not Matched')
    return render(request,'student/student_otp.html')

def student_change_pw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            un = request.session.get('studentun')
            UO = User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('student_login'))
        return HttpResponse('password Not Matched')
    return render(request,'student/student_change_pw.html')