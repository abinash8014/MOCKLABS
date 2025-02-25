from django.urls import path
from student.views import *

urlpatterns = [
    path('student_home/',student_home,name='student_home'),
    path('student_register/',student_register,name='student_register'),
    path('student_login/',student_login,name='student_login'),
    path('student_logout/',student_logout,name='student_logout'),
    path('see_schedule/',see_schedule,name='see_schedule'),
]
