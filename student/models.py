from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os 

# Create your models here.

def get_upload_path(self,filename):
    extension = filename.split('.')[-1]
    filename = f"{self.username.first_name}_{self.username.last_name}_resume.{extension}"
    return os.path.join('student_resumes',filename)

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
    resume = models.FileField(upload_to=get_upload_path,validators=[FileExtensionValidator(['pdf','docx'])])
    
    def __str__(self):
        return self.username.username