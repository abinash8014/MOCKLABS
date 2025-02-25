from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentRating(models.Model):
    subjects = [
        ('Python','Python'),
        ('Java','Java'),
        ('MongoDB','MongoDB'),
        ('React js','Reactjs'),
        ('ExpressJs','ExpressJs'),
        ('Nodejs','Nodejs'),
        ('SQL','SQL'),
        ('WEB_TECH','WEB_TECH'),
        ('DJango','Django'),
        ('Spring','Spring'),
        ('HyberNet','HyberNet'),
        ('SpringBoot','SpringBoot'),
    ]
    Ratings = [
        ('*','*'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
    ]
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rating')
    subject = models.CharField(max_length=100,choices=subjects,default='Python')
    Technical = models.CharField(max_length=200,choices=Ratings,default='1')
    Communication = models.CharField(max_length=100,choices=Ratings,default='1')
    Programming = models.CharField(max_length=50,choices=Ratings,default='1')
    remarks = models.CharField(max_length=200)
    conducted_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='by')
    conducted_on = models.DateField(auto_now=True, auto_now_add=False)
    
    
    def __str__(self):
        return self.student.username