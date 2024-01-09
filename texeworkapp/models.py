from django.db import models
from datetime import datetime,date, timedelta

from texeclientapp.models import *

# work app connection 

from texecrmapp.models import *
# Create your models here.


class user_registration(models.Model):
    regno= models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    number = models.CharField(max_length=250, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    profile = models.ImageField(upload_to='images/propic',null=True, blank=True, default="static\images\static_image\icon.svg")
    joindate = models.DateField(null=True, default=date.today())
    last_login = models.DateTimeField(null=True, blank=True)  
    status =models.CharField(max_length = 255,blank=True,null=True, default="active")
    addres =  models.TextField(blank=True,null=True)
    role = models.CharField(max_length=255,blank=True,null=True)
    dob=models.DateField(null=True,)
    location = models.CharField(max_length=250, null=True, blank=True)
    otp= models.CharField(max_length=250, null=True, blank=True)
    designation=models.CharField(max_length=250, null=True, blank=True)
    complaint=models.CharField(max_length=250, null=True, blank=True)
    orders=models.CharField(max_length=250, null=True, blank=True)
    preformance=models.CharField(max_length=250, null=True, blank=True)
    def get_email_field_name(self):
        return 'email'


class order_management(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.SET_NULL, null=True, blank=True)
    order_crm = models.ForeignKey(orders_crm, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(orders, on_delete=models.SET_NULL, null=True, blank=True)
    start_time=models.DateTimeField(null=True, blank=True, default=datetime.now())
    end_time=models.DateTimeField(null=True, blank=True)
    time_taken=models.CharField(max_length=255, null=True, blank=True)
    work_status=models.CharField(max_length=255, null=True, blank=True)
    




