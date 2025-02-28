from django.urls import path
from hr.views import *

urlpatterns = [
    path('hr_home/',hr_home,name='hr_home'),
    path('hr_login/',hr_login,name='hr_login'),
    path('hr_logout/',hr_logout,name='hr_logout'),
    path('mock_ratings/',mock_ratings,name='mock_ratings'),
    path('hr_forget_pw/',hr_forget_pw,name='hr_forget_pw'),
    path('hr_otp/',hr_otp,name='hr_otp'),
    path('hr_change_pw/',hr_change_pw,name='hr_change_pw'),
    path('schedule_mock/',schedule_mock,name='schedule_mock')
]
