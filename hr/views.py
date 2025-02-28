from django.shortcuts import render
from manager.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from hr.forms import *
import random
from django.core.mail import send_mail
import csv

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

def hr_forget_pw(request):
    if request.method == "POST":
        un = request.POST.get('un')
        # UO = User.objects.filter(username=un, is_staff=True, is_superuser=False).first()
        UO = User.objects.get(username=un)
        EO = EmployeeProfile.objects.get(username=UO)
        
        if UO and UO.is_active:
            if UO.is_staff and EO.Role == 'HR':
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
                request.session['hrotp'] = otp
                request.session['hrun'] = un
                return HttpResponseRedirect(reverse('hr_otp'))
            return HttpResponse('User objects is not there')
        
        return HttpResponse('User not found or not an HR')
    
    return render(request,'hr/hr_forget_pw.html')


def hr_otp(request):
    if request.method == 'POST':
        eotp=request.POST.get('otp')
        gotp=request.session.get('hrotp')
        un = request.session.get('hrun')
        if int(eotp)==gotp:
            UO = User.objects.get(username=un)
            login(request,UO)
            return HttpResponseRedirect(reverse('hr_change_pw'))
        return HttpResponse('Otp not Matched')
    return render(request,'hr/hr_otp.html')

def hr_change_pw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            username = request.session.get('hrun')
            UO = User.objects.get(username=username)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('hr_login'))
        return HttpResponse('password Not Matched')
    return render(request,'hr/hr_change_pw.html')

@hr_login_required
def schedule_mock(request):
    un = request.session.get('hrun')
    print(un)
    UO = User.objects.get(username=un)
    PO = EmployeeProfile.objects.get(username=UO)
    ESFO = SchedulingForm()
    d = {'ESFO': ESFO}
    if request.method == 'POST' and request.FILES:
        SFDO = SchedulingForm(request.POST, request.FILES)
        if SFDO.is_valid():
            SFDO.save()
            with open(r"C:\Users\Abinash Sahoo\OneDrive\Desktop\Book 1(Sheet1).csv",'r') as f:
                datas = csv.reader(f)
                usernames = [i[1]+i[2] for i in datas]
                for un in usernames:
                    SO = User.objects.get(username=un)
                    print(SO)
                message = f'''I hope you’re doing well! We are excited to invite you for a mock interview as part of your preparation for the  at QSpiders BBSR. This session is designed to help you practice and receive constructive feedback before your official interview.

Interview Details:
📅 Date: {SFDO.cleaned_data.get('date')}
⏰ Time: {SFDO.cleaned_data.get('time')}
📍 Location/Platform: QSpiders Bhubaneswar
⏳ Duration: 30min

During the mock interview, we will focus on {SFDO.cleaned_data.get('subject')}, followed by a feedback session.

Please confirm your availability at your earliest convenience. Feel free to reach out if you have any questions. We look forward to helping you prepare!

Best regards,
{UO.first_name}
{PO.Role}
QPsiders BBSR
{PO.pno}'''
                send_mail(
                    'RE:Invitation for Mock Interview - QSpiders Bhubaneswar {PO.username}',
                    message,
                    'abinashsahoo063@gmail.com',
                    [UO.email],
                    fail_silently=False
                )
            return HttpResponseRedirect(reverse('hr_home'))
        return HttpResponse('Invalid Data')
    
    # with open(r"C:\Users\Abinash Sahoo\OneDrive\Desktop\Book 1(Sheet1).csv", 'r') as file:
    #     csv_reader = csv.reader(file)
    #     next(csv_reader)
    #     email = [i[4] for i in csv_reader] 
    #     print(email)    

    # with open(r"C:\Users\Abinash Sahoo\OneDrive\Desktop\Book 1(Sheet1).csv", 'r') as file:
    #     csv_reader = csv.reader(file)
    #     next(csv_reader)
    #     username = [i[1]+i[2] for i in csv_reader]
    #     print(username)                                                                                      
    return render(request, 'hr/schedule_mock.html',d)