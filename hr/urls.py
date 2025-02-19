from django.urls import path
from hr.views import *

urlpatterns = [
    path('hr_home/',hr_home,name='hr_home'),
    path('hr_login/',hr_login,name='hr_login'),
    path('hr_logout/',hr_logout,name='hr_logout'),
]
