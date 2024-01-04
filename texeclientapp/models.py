from django.db import models
from datetime import datetime,date, timedelta
# Create your models here.

class registration(models.Model):
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
    pin = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    otp= models.CharField(max_length=250, null=True, blank=True)
    def get_email_field_name(self):
        return 'email'

	

class banner(models.Model):
    top_banner1 = models.ImageField(upload_to='images/banner',null=True, blank=True)
    top_link1 = models.CharField(max_length=250, null=True, blank=True)

    top_banner2 = models.ImageField(upload_to='images/banner',null=True, blank=True)
    top_link2 = models.CharField(max_length=250, null=True, blank=True)

    top_banner3 = models.ImageField(upload_to='images/banner',null=True, blank=True)
    top_link3 = models.CharField(max_length=250, null=True, blank=True)
    middle_banner = models.ImageField(upload_to='images/banner',null=True, blank=True)
    middle_link = models.CharField(max_length=250, null=True, blank=True)
    bottom_banner1 = models.ImageField(upload_to='images/banner',null=True, blank=True)
    bottom_link1 = models.CharField(max_length=250, null=True, blank=True)
    bottom_banner2 = models.ImageField(upload_to='images/banner',null=True, blank=True)
    bottom_link2 = models.CharField(max_length=250, null=True, blank=True)


class category(models.Model):
    category_name=  models.CharField(max_length=255,blank=True,null=True)
    def _str_(self):
        return self.category_name

class sub_category(models.Model):
    subcategory=  models.CharField(max_length=255,blank=True,null=True)
    category=models.ForeignKey(category, on_delete=models.SET_NULL, null=True, blank=True)
    buying_count=models.IntegerField(default=0)

class item(models.Model):
    user = models.ForeignKey(registration, on_delete=models.SET_NULL, null=True, blank=True)
    category= models.ForeignKey(category, on_delete=models.SET_NULL, null=True, blank=True,default=None)
    sub_category= models.ForeignKey(sub_category, on_delete=models.SET_NULL, null=True, blank=True,default=None)
    name = models.CharField(max_length=255,blank=True,null=True)
    title_description = models.CharField(max_length=100,blank=True,null=True)
    price = models.FloatField(default=0)
    offer_price=  models.FloatField(default=0)
    buying_count = models.IntegerField(default=0)
    offer = models.IntegerField(default=0)
    image = models.FileField(upload_to='images/items', default='static/images/logo/noimage.jpg')
    subcategory=models.CharField(max_length=255,blank=True,null=True)
    custom=models.CharField(max_length=255,blank=True,null=True)
    size_chart = models.FileField(upload_to='images/size', default='static/round_neck.jpg')

class sub_color(models.Model):
    color=  models.FileField(upload_to='images/items', null=True, blank=True)
    item=models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)

class sub_size(models.Model):
    size=  models.CharField(max_length=255,blank=True,null=True)
    item=models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)

class sub_images(models.Model):
    image=  models.FileField(upload_to='images/sub_items', default='static/images/logo/noimage.jpg')
    item=models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)

class cart(models.Model):
    user = models.ForeignKey(registration, on_delete=models.SET_NULL, null=True, blank=True)
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

class orders(models.Model):
    regno= models.CharField(max_length=250, null=True, blank=True)
    user = models.ForeignKey(registration, on_delete=models.SET_NULL, null=True, blank=True)
    status =models.CharField(max_length = 255,blank=True,null=True, default=0)
    total_amount=models.FloatField(default=0,null=True, blank=True)
    date=models.DateTimeField(null=True, blank=True)
    stage_count=models.IntegerField(default=0,null=True, blank=True)
    stage =models.CharField(max_length = 255,blank=True,null=True)
    delivery_date=models.DateField(null=True, blank=True)

class checkout_item(models.Model):
    orders = models.ForeignKey(orders, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(cart, on_delete=models.SET_NULL, null=True, blank=True)

    item_name= models.CharField(max_length=255,blank=True,null=True)
    qty=models.IntegerField(null=True, blank=True)
    item_price=models.FloatField(null=True, blank=True)

class wishlist(models.Model):
    user = models.ForeignKey(registration, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)



class events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True,null=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    user=models.ForeignKey(registration, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(orders, on_delete=models.SET_NULL, null=True, blank=True)
    
