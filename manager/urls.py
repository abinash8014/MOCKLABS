from django.urls import *
from manager.views import *

urlpatterns = [
    path('manager_home/',manager_home,name='manager_home'),
    path('add_employee/',add_employee,name='add_employee'),  
    path('manager_login/',manager_login,name='manager_login'),
    path('manager_logout/',manager_logout,name='manager_logout'),
    path('manager_forget_pw/',manager_forget_pw,name='manager_forget_pw'),
    path('manager_otp/',manager_otp,name='manager_otp'),
    path('manager_change_pw/',manager_change_pw,name='manager_change_pw'),
]
