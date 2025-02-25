from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmployeeProfile(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    pno = models.CharField(max_length=100)
    Role = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username.username
