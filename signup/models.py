from pickle import FALSE
from django.db import models
from django.contrib.auth.models import User
from signup.constants import GENDER_CHOICES

# Create your models here.

class User_details(models.Model):
    user_detail = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_num = models.IntegerField(max_length=20,)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2)
    address = models.TextField(max_length=1600)
    is_suspend = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now=False)
    
    def __str__(self):
        return self.address
    
    def user_contact(self):
        return self.user_detail


class DBO(User_details):
    namesd=  models.TextField(max_length=1600)