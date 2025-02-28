from django.urls import path
from trainer.views import *

urlpatterns = [
    path('trainer_home/',trainer_home,name='trainer_home'),
    path('trainer_login/',trainer_login,name='trainer_login'),
    path('trainer_logout/',trainer_logout,name='trainer_logout'),
    path('start_mock/',start_mock,name='start_mock'),
    path('trainer_forget_pw/',trainer_forget_pw,name='trainer_forget_pw'),
    path('trainer_otp/',trainer_otp,name='trainer_otp'),
    path('trainer_change_pw/',trainer_change_pw,name='change_pw'),
]
