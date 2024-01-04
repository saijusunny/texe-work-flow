
from django.db import models
from datetime import datetime,date, timedelta
# clientapp connection

from texeclientapp.models import item
from texeclientapp.models import sub_images
from texeclientapp.models import sub_color
# work app connection 

from texeworkapp.models import *


class users(models.Model):
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

class complaint_service(models.Model):
    
    users = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, blank=True)
    regno= models.CharField(max_length=255,blank=True,null=True)
    complaint = models.TextField(blank=True,null=True)
    status= models.CharField(max_length=255,blank=True,null=True)
    date_register= models.DateField(default=date.today())
    type= models.CharField(max_length=255,blank=True,null=True)



class cart_crm(models.Model):
    user = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(sub_images, on_delete=models.SET_NULL, null=True, blank=True)
    size= models.CharField(max_length=255,blank=True,null=True)
    color= models.CharField(max_length=255,blank=True,null=True)
    meterial= models.CharField(max_length=255,blank=True,null=True)
    design= models.FileField(upload_to='images/cart/design',null=True, blank=True)
    logo= models.FileField(upload_to='images/cart/logos',null=True, blank=True)
    name= models.CharField(max_length=255,blank=True,null=True)
    number= models.CharField(max_length=255,blank=True,null=True)
    status= models.CharField(max_length=255,blank=True,null=True)
    sub_color= models.ForeignKey(sub_color, on_delete=models.SET_NULL, null=True, blank=True)

class orders_crm(models.Model):
    regno= models.CharField(max_length=250, null=True, blank=True)
    user = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, blank=True)
    status =models.CharField(max_length = 255,blank=True,null=True)
    total_amount=models.FloatField(default=0,null=True, blank=True)
    date=models.DateTimeField(null=True, blank=True)
    stage_count=models.IntegerField(default=0,null=True, blank=True)
    stage =models.CharField(max_length = 255,blank=True,null=True)
    delivery_date=models.DateField(null=True, blank=True)

    

class checkout_item_crm(models.Model):
    orders = models.ForeignKey(orders_crm, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(cart_crm, on_delete=models.SET_NULL, null=True, blank=True)

    item_name= models.CharField(max_length=255,blank=True,null=True)
    qty=models.IntegerField(null=True, blank=True)
    item_price=models.FloatField(null=True, blank=True)

class events_crm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True,null=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    user=models.ForeignKey(users, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(orders_crm, on_delete=models.SET_NULL, null=True, blank=True)