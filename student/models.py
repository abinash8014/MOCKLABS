from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentProfile(models.Model):
    courses = [
        ('Python Full Stack','Python Full Stack'),
        ('Java Full Stack','Java Full Stack'),
        ('MERN Full Stack','MERN Full Stack'),
        ('FullStack Testing','FullStack Testing')
    ]
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    pno = models.CharField(max_length=50)
    add = models.CharField(max_length=50)
    course = models.CharField(max_length=50,choices=courses,default='Python Full Stack')
    profile_pic = models.ImageField(upload_to='student_profiles/')
    resume = models.FileField(upload_to='student_resumes/')
    
    def __str__(self):
        return self.username.username