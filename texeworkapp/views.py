from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *

from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
import random
import string

from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from django.urls import resolve
# from requests import request


# clientapp connection
from texeclientapp.views import *
from texeclientapp.models import *

# work app connection 
from texecrmapp.views import *
from texecrmapp.models import *

from datetime import datetime, timedelta
from django.utils import timezone
# pip install schedule
import threading
import time
def login(request):
    if request.method == "POST":
        username  = request.POST.get('use')
        password = request.POST.get('pass')
        print(username)
        user = authenticate(username=username, password=password)
        try:
            if user_registration.objects.filter(email=username, password=password,role="staff").exists():

                    member = user_registration.objects.get(email=username, password=password)
                    request.session['userid'] = member.id
                    return redirect('staff_index')
            elif users.objects.filter(email=username, password=password,role="user").exists():
                member = users.objects.get(email=username, password=password)
                request.session['userid'] = member.id
                return redirect('user_dashboard')
            elif user.is_superuser:
                request.session['userid'] = request.user.id
                return redirect('dashboard')
            
            else:
            
                messages.error(request, 'Invalid username or password')
        except:
            messages.error(request, 'Invalid username or password')
    return render(request, 'home/login.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if  users.objects.filter(email=email).exists():
            user =  users.objects.get(email=email)

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('forget-password/reset_password_email.html',{
                'user':user,
                'domain' :current_site,
                'user_id' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }) 

            to_email = email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()

            messages.success(request,"Password reset email has been sent your email address.")
            return redirect('login')
        else:
            messages.error(request,"This account does not exists !")
            return redirect('forgotPassword')
    return render(request,'forget-password/forgotPassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user =  users._default_manager.get(pk=user_id)  
    except(TypeError,ValueError,OverflowError, registration.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['user_id'] = user_id 
        messages.success(request,"Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request,"The link has been expired !")
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('user_id') 
            user =  users.objects.get(pk=uid)
            user.password = password
            user.save()
            messages.success(request,"Password reset successfull.")
            return redirect('login')

        else:
            messages.error(request,"Password do not match")
            return redirect('resetPassword')
    else:
        return render(request,'forget-password/resetPassword.html')




def dashboard(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
   
    data = item.objects.all()
    sub_cat=sub_category.objects.all()
    today = datetime.now()
    sub=orders.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
    event=events.objects.filter(start__date=date.today())
    print(event)
    nm=[]
    cnt=[]
    for i in sub:
        
        nm.append(i)
        qty=orders.objects.filter(date__day=i).count()
        cnt.append(qty)

    sub2=orders_crm.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
    for i in sub2:
        
        nm.append(i)
        qty=orders_crm.objects.filter(date__day=i).count()
        cnt.append(qty)
    
    staff=user_registration.objects.all()
    print(staff)
 
    return render(request,'home/index.html',{'segment':segment,'sub_cat':sub_cat,'nm':nm,
        'cnt':cnt,'data': data,'event':event, 'staff':staff})

def get_date_event(request):
    day = request.GET.get('day')
    month = request.GET.get('month')
    year = request.GET.get('year')
    all_event = events.objects.filter(start__day=day, start__month=month, start__year=year)
    names = [obj.name for obj in all_event]
    strt = [obj.start.hour for obj in all_event]
    ends = [obj.end.hour for obj in all_event]
   
    return JsonResponse({"status":" not","strt": strt,"ends":ends,"names":names})

def icons(request):
    return render(request,"home/icons.html")
    
def filter_date_event(request):
    if request.method=="POST":
        dates=request.POST.get('date_filter',None)
        segment="dashboard"
       
        data = item.objects.all()
        sub_cat=sub_category.objects.all()
        today = datetime.now()
        sub=orders.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
        event=events.objects.filter(start=dates)

        nm=[]
        cnt=[]
        for i in sub:
            
            nm.append(i)
            qty=orders.objects.filter(date__day=i).count()
            cnt.append(qty)

        
    
        return render(request,'home/index.html',{'segment':segment,'sub_cat':sub_cat,'nm':nm,
            'cnt':cnt,'data': data,'event':event})
    return redirect('dashboard')

def create_event(request):
    if request.method=="POST":
        st_dt=request.POST.get('start_dt',None)
        end_dt=request.POST.get('end_dt',None)
        text=request.POST.get('event_des',None)
        ev=events()
        ev.name=request.POST.get('event_des',None)
        ev.start=request.POST.get('start_dt',None)
        ev.end=request.POST.get('end_dt',None)
        ev.save()
        return redirect('dashboard')
        
    return redirect('dashboard')

def registrations(request):

    user=complaint_service.objects.all().count()
    reg=registration.objects.all().count()
    orde=orders.objects.get(id=24)

    texeclietapp_response = regist(request)
    workss = worksssddd(request)

    
    return render(request,'accounts/register.html')

def staff_home(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    staffs=user_registration.objects.filter(role="staff")

    return render(request,'home/staff_home.html',{'segment':segment,'staffs':staffs})

def add_staff(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    
    if request.method=="POST":
        user_reg=user_registration.objects.all().last()
        dt= date.today()
        digits = string.digits
        otp = ''.join(random.choices(digits, k=6))
        if user_reg:
            regst=int(user_reg.id)+1
        else:
            regst=1
        usr=user_registration()
        em=request.POST.get('email', None)
        if user_registration.objects.filter(email=em).exists():
           
            messages.error(request,"Email Already exists !")
            return redirect('add_staff')
        else:
            usr.regno= "STF"+str(regst)+str(dt.day)+str(dt.year)[-2:]
            usr.name=request.POST.get('name', None)
            usr.addres=request.POST.get('address', None)
            usr.number=request.POST.get('phn_no', None)
            if request.FILES.get('propic', None) == None:
                usr.profile= 'static\images\static_image\icon.svg'
            else:

                usr.profile=request.FILES.get('propic', None)
            usr.email=request.POST.get('email', None)
            usr.location=request.POST.get('location', None)
            usr.designation=request.POST.get('desi', None)
            usr.dob=request.POST.get('dob', None)
            usr.status="active"
            usr.role="staff"
            usr.password=otp
            usr.complaint=request.POST.get('complaintss',None)
            usr.orders=request.POST.get('order',None)
            usr.preformance="0"
            usr.joindate=date.today()
            usr.save()
            current_site = get_current_site(request)
            mail_subject = "Texe Registration Success"
            message = f"Hai {usr.name},\n\nUser name : {em}\nPassword : {otp}\nClick the link {current_site} to log in to your account."

            to_email = usr.email
          
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()
        return redirect('staff_home')


    return render(request,'home/add_staff.html',{'segment':segment,})


def edit_staff(request,id):

    usr_client=user_registration.objects.get(id=id)
    
    return render(request,'home\edits_staff.html',{'usr_client':usr_client})
 

def save_edit_staff(request,id):
    usr=user_registration.objects.get(id=id)

    if request.method=="POST":
        
        em=request.POST.get('email', None)
    
        
        usr.name=request.POST.get('name', None)
        usr.addres=request.POST.get('address', None)
        usr.number=request.POST.get('phn_no', None)
        if request.FILES.get('propic', None) == None:
            pass
        else:

            usr.profile=request.FILES.get('propic', None)
        usr.email=request.POST.get('email', None)
        usr.location=request.POST.get('location', None)
        usr.designation=request.POST.get('desi', None)
        usr.dob=request.POST.get('dob', None)
        usr.status=request.POST.get('status', None)
        usr.complaint=request.POST.get('complaintss',None)
        usr.orders=request.POST.get('order',None)
    
        usr.save()
        
        return redirect('staff_home')


    return redirect('staff_home')
def delete_staff(request,id):
    usr=user_registration.objects.get(id=id)
    usr.delete()
    return redirect('staff_home')



def orders_dta(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
  
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    context={
            'segment':segment,
     
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    return render(request, 'home/orders.html', context)

def filter_order(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="orders_dta"
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()
        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
           
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/orders.html', context)


def filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="orders_dta"
      
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
       
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/orders.html', context)


def pending_orders(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
   
    orde=orders_crm.objects.filter(stage="pending").order_by("-id")
    
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="pending").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    context={
            'segment':segment,
           
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    return render(request, 'home/pending_orders.html', context)

def filter_pending(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="orders_dta"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="pending")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="pending")
        ord_item_client=checkout_item.objects.all()
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
          
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/pending_orders.html', context)


def filter_pending_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="pending" )
        ord_item=checkout_item_crm.objects.all()
        segment="orders_dta"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="pending" )
        ord_item_client=checkout_item.objects.all()
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
       
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/pending_orders.html', context)



def today_orders(request):
    resolved_func = resolve(request.path_info).func
    segment="orders_dta"

    orde=orders_crm.objects.filter(date__date=date.today())
    
    ord_item=checkout_item_crm.objects.all()
    orde_client=orders.objects.filter(date__date=date.today())
    ord_item_client=checkout_item.objects.all()
    print(orde_client)
    context={
            'segment':segment,
   
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    return render(request, 'home/today_orders.html', context)


def delivery_today(request):
    resolved_func = resolve(request.path_info).func
    segment="orders_dta"
   
    orde=orders_crm.objects.filter(date__date=date.today())
    
    ord_item=checkout_item_crm.objects.all()
    orde_client=orders.objects.filter(delivery_date=date.today())
    ord_item_client=checkout_item.objects.all()
    print(orde_client)
    context={
            'segment':segment,
        
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    return render(request, 'home\delivery_today.html', context)

def delivery_tomorrow(request):
    resolved_func = resolve(request.path_info).func
    segment="orders_dta"
  

    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    orde=orders_crm.objects.filter(delivery_date=tomorrow.date())
    
    ord_item=checkout_item_crm.objects.all()
    orde_client=orders.objects.filter(delivery_date=tomorrow.date())
    ord_item_client=checkout_item.objects.all()
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    return render(request, 'home\delivery_tomorrow.html', context)

def up_expect(request):
    ele = request.GET.get('ele')
    count = request.GET.get('count')
    itm=orders.objects.get(regno=ele)
    itm.delivery_date=count
    itm.save()
    return JsonResponse({"status":" not"})

def up_expect_crm(request):
    print("sdfsfdsfjjffdgjdsdfsdfs")
    ele = request.GET.get('ele')
    count = request.GET.get('count')
    itm=orders_crm.objects.get(id=ele)
    itm.delivery_date=count
    itm.save()
    return JsonResponse({"status":" not"})

def filter_today_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id, date__date=date.today())
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,date__date=date.today() )
        ord_item_client=checkout_item.objects.all()
        
        segment="orders_dta"
       
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
      
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/today_orders.html', context)


def change_order_status(request):
    ele = request.GET.get('ele')
    count = request.GET.get('count')
    itm=orders_crm.objects.get(id=ele)

    itm.stage_count=count
    if int(count)==6:
        itm.status='arrived'
        itm.stage="arrived"
    else:
        itm.status='delivery'
        itm.stage="despatch"
    itm.save()
    return JsonResponse({"status":" not"})


def change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    print(ele)
    itm=orders.objects.get(regno=ele)

    itm.stage=stg
    itm.save()
    return JsonResponse({"status":" not"})


def change_order_status_client(request):
    ele = request.GET.get('ele')
    count = request.GET.get('count')
    itm=orders.objects.get(regno=ele)

    itm.stage_count=count
    if int(count)==6:
        itm.status='arrived'
        itm.stage="arrived"
    else:
        itm.status='delivery'
        itm.stage="despatch"
    itm.save()
    return JsonResponse({"status":" not"})



def change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    itm=orders_crm.objects.get(id=ele)

    itm.stage=stg
    itm.save()
    return JsonResponse({"status":" not"})


def orders_list(request,id):
    orde = orders_crm.objects.filter(id=id).order_by("-id")
    ord_item=checkout_item_crm.objects.filter(orders=id)
    
    segment="orders_dta"
   
    context={
        "orders":orde,
        "ord_item":ord_item,
        'segment':segment,
        'ord_ids':id,
      
    }
    return render(request, 'home/orders_list.html', context)

def orders_list_client(request,id):
    orde = orders.objects.filter(id=id).order_by("-id")
    ord_item=checkout_item.objects.filter(id=id)
 
    segment="orders_dta"

    context={
        "orders":orde,
        "ord_item":ord_item,
        'segment':segment,
        'ord_ids':id,
   
    }
    return render(request, 'home/orders_list_client.html', context)

def prouct_list(request):
    segment="orders_dta"
 
    

    items=item.objects.all()
    return render(request, 'home/product_list.html', {'items':items,'segment':segment})

def view_items_orders(request,id):
    segment="orders_dta"

    names=users.objects.filter(role="user")
   
    dt= date.today()
    cmp_reg=orders.objects.all().last()
    if cmp_reg:
        regst=int(cmp_reg.id)+1
    else:
        regst=1
    regss="ORD"+str(0)+str(regst)+str(dt.day)+str(dt.year)[-2:]

    items=item.objects.get(id=id)
    sub=sub_images.objects.filter(item=items)
    color=sub_color.objects.filter(item=id)
    size=sub_size.objects.filter(item=id)
    
    
    context={
            'segment':segment,
      
    
            'items':items,
            'sub':sub,
            'color':color,
            'size':size,
            'names':names,
            'regss':regss,
            'ids':id

        }
    return render(request, 'home/view_items_orders.html', context)


def add_user_order(request,id):
    user_reg=users.objects.all().last()

    segment="orders_dta"
 
    if request.method=='POST':
        urs=users()
        dt= date.today()
        digits = string.digits
        otp = ''.join(random.choices(digits, k=6))
        if user_reg:
            regst=int(user_reg.id)+1
        else:
            regst=1
        urs.regno= "CUS"+str(regst)+str(dt.day)+str(dt.year)[-2:]
        urs.name = request.POST.get('name',None)
        urs.email = request.POST.get('email',None)
        urs.number = request.POST.get('phn_no',None)
        urs.password = otp
        if request.FILES.get('propic',None)=="":
            pass
        else:
            profile = request.FILES.get('propic',None)
        urs.joindate = date.today()
        urs.status ="active"
        urs.addres =  request.POST.get('address',None)
        urs.role = "user"
        urs.save()
        return redirect('view_items_orders',id)
    return render(request, 'home/add_user_order.html', {'segment':segment})

def save_cart(request,id):
    
    if request.method=="POST":
        ids=request.POST.get('name',None)
        usr=users.objects.get(id=ids)
        
        itm=item.objects.get(id=id)
        colors=sub_color.objects.filter(item=itm).first()

        sizes=sub_size.objects.filter(item=itm).first()
        if request.POST.get('cart_id',None) == "":
            carts=cart_crm()
            
            carts.user = usr
            carts.item_id = itm.id
            carts.size= sizes.size
            carts.color=colors.color
            carts.sub_color_id=colors.id
            carts.meterial= "Cotton"
            carts.status="cart"
            carts.design= request.FILES.get('design',None)
            carts.logo= request.FILES.get('logo',None)
            carts.name= request.POST.get('text',None)
            carts.number= request.POST.get('number',None)
            mdl_id=request.POST.get('model_num1', None)
            mdl=sub_images.objects.get(id=mdl_id)
            carts.model_id = mdl.id
            carts.save()
           
        else:
            
            cart_id=request.POST.get('cart_id',None)
            crt=cart_crm.objects.get(id=cart_id)
            if crt.size==None:
                crt.size= sizes.size
            else:
                pass
            if crt.color==None:
                crt.color= colors.color
                crt.sub_color_id=colors.id
            else:
                pass


            if crt.meterial==None:
                crt.meterial= "Cotton"
            else:
                pass
            if crt.model==None:
                mdl_id=request.POST.get('model_num1', None)
                mdl=sub_images.objects.get(id=mdl_id)
                crt.model_id = mdl.id
            else:
                pass
            
            crt.design= request.FILES.get('design',None)
            crt.logo= request.FILES.get('logo',None)
            crt.name= request.POST.get('text',None)
            crt.number= request.POST.get('number',None)
            crt.status="cart"
            crt.save()

        # order_ save


        total_amount = itm.offer_price
        numb= request.POST.get('regno',None)
        

        chk=orders_crm()
        chk.user = usr
        chk.total_amount=total_amount
        chk.date=datetime.now()
        chk.status="checkout"
        chk.regno=numb
        chk.stage="pending"
        chk.save()
        item_id =id
        qty =request.POST.get('qty',None)
        if request.POST.get('cart_id',None) == "":
            cart_id=carts.id
            
        else:
            cart_id=request.POST.get('cart_id',None)

      
        itm=item.objects.get(id=item_id)
        itm.buying_count=int(itm.buying_count+1)
        itm.save()
        
        sub=sub_category.objects.get(id=itm.sub_category.id)
        
        sub.buying_count=int(sub.buying_count)+1
        sub.save()

        crts= cart_crm.objects.get(id=cart_id)
        crts.status="checkout"
        crts.save()
        tot=float(itm.offer_price)*int(qty)
        created = checkout_item_crm.objects.create(item_id=itm.id,qty=qty,item_name=itm.name,item_price=tot, orders=chk, cart_id=crts.id)

        chk_item=checkout_item_crm.objects.filter(orders=chk)

        start = datetime.now()


        date_obj = date.strftime(start, "%Y-%m-%d %H:%M:%S")
        # one_hour = timedelta(hours=1)
        # new_date_obj = date_obj + one_hour
        # end = new_date_obj.strftime("%    Y-%m-%d %H:%M:%S.%f")


        title=str(numb)+" "+str(usr.name) 
        event = events_crm(name=title, start=start,end=start, user=usr, order=chk) 
        event.save()

        current_site = get_current_site(request)
        mail_subject = "Texe Order Placed"
        message = f"Hai {usr.name},\n\nUser name : {usr.email}\nPassword : {usr.password}\nOrder Number : {numb}\nClick the link {current_site} to view your order status"

        to_email = usr.email
        send_email = EmailMessage(mail_subject,message,to = [to_email])
        send_email.send()



        return redirect('orders_dta')


    return redirect('orders_dta')


def cart_cust_size(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    print(cart_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model = None
    else:
        crt=cart_crm.objects.get(id=cart_id)

    
    crt.size= ele
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})

def cart_change_color(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    idsr=request.GET.get('id')
    itm=item.objects.get(id=prd_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model = None
    else:
        crt=cart_crm.objects.get(id=cart_id) 

    
    crt.color= ele
    print(idsr)
    idata=sub_color.objects.get(id=idsr)
    crt.sub_color_id=idata.id
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})

def cart_change_meterial(request):
    ele = request.GET.get('ele')
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
  
    itm=item.objects.get(id=prd_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model = None
    else:
        crt=cart_crm.objects.get(id=cart_id) 

    
    crt.meterial= ele
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})


def cart_change_model(request):
    ele = request.GET.get('ele')
    
    model=sub_images.objects.get(id=ele)
    cart_id = request.GET.get('cart_id')
    prd_id = request.GET.get('prd_id')
    itm=item.objects.get(id=prd_id)
    ids=request.GET.get('usrs')
    usr=users.objects.get(id=ids)
    if cart_id=="":
        crt=cart_crm()
        crt.user = usr
        crt.item_id = itm.id
        crt.model_id = model.id
    else:
        crt=cart_crm.objects.get(id=cart_id) 

    
    crt.model_id = model.id
    crt.save()
    return JsonResponse({"status":" not", "ids":crt.id})


def order_managements(request):
    return render(request, 'home/order_management.html')



def payment_pending_orders(request):
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
 
    orde=orders_crm.objects.filter(stage="payment").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="payment").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']='home/payment_pending_orders.html'
    context={
            'segment':segment,
            'stg':"Payment pending orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/payment_pending_orders.html', context)

def filter_payment_pending(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="orders_dta"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="payment")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="payment")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Payment pending orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/payment_pending_orders.html', context)


def filter_payment_pending_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="payment" )
        ord_item=checkout_item_crm.objects.all()
        segment="orders_dta"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="payment" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Payment pending orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/payment_pending_orders.html', context)

def payment_completed_crm(request,id):
    itm=orders_crm.objects.get(id=id)
    itm.stage="pending"
    itm.save()
    return redirect('payment_pending_orders')

def payment_completed_client(request,id):
    itm=orders_crm.objects.get(id=id)
    itm.stage="pending"
    itm.save()
    return redirect('payment_pending_orders')


def pending_orders_mang(request):
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
 
    orde=orders_crm.objects.filter(stage="pending").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="pending").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    context={
            'segment':segment,
            'stg':"Pending orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/pending_payment.html',context)


def filter_pending_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="orders_dta"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="pending")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="pending")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Pending orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/pending_payment.html', context)


def filter_pending_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="pending" )
        ord_item=checkout_item_crm.objects.all()
        segment="orders_dta"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="pending" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Pending orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/pending_payment.html', context)



#####!*/**/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/* For Design - Admin
def orders_list_designer(request,id):
    orde = orders_crm.objects.filter(id=id).order_by("-id")
    ord_item=checkout_item_crm.objects.filter(orders=id)
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    segment="order_managements"
 
    context={
        "orders":orde,
        "ord_item":ord_item,
        'segment':segment,
        'ord_ids':id,
    
    }
    return render(request, 'home/orders_list_designer.html', context)

def orders_list_designer_client(request,id):
    orde = orders.objects.filter(id=id).order_by("-id")
   
    ord_item=checkout_item.objects.filter(id=id)
    print(ord_item.count())
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
 
    segment="order_managements"
  
    orde_stat = orders.objects.get(id=id)
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
        "orders":orde,
        "ord_item":ord_item,
        'segment':segment,
 
        'ord_ids':id,
        'orde_stat':orde_stat,
    }
    return render(request, 'home/orders_list_designer_client.html', context)

def get_staff_list(request):
    dep = request.GET.get('dep')

    staff_st=user_registration.objects.filter(designation=dep)
    data = list(staff_st.values())
 
    return JsonResponse({"status":" not", "data":data})

def save_assign_stage(request, id):
    if request.method=="POST":
        ors= order_management()
        urs= request.POST.get('stage_staff')
        ords=orders.objects.get(id=id)
        idrs=user_registration.objects.get(id=urs)
        ors.user=idrs
        ors.order_id=id
        ors.work_status="working"
        ors.order_no=ords.regno
        ors.save()
        orde_stat = orders.objects.get(id=id)
        orde_stat.stage=request.POST.get('stage')
        orde_stat.save()
        
        return redirect(request.session['previous_url'])
    return redirect('orders_list_designer_client', id)

def save_assign_stage_crm(request, id):
    if request.method=="POST":
        ors= order_management()
        urs= request.POST.get('stage_staff')
        ords=orders_crm.objects.get(id=id)
        idrs=user_registration.objects.get(id=urs)
        ors.user=idrs
        ors.order_crm_id=id
        ors.work_status="working"
        ors.order_no=ords.regno
        ors.save()
        orde_stat = orders_crm.objects.get(id=id)
        orde_stat.stage=request.POST.get('stage')
        orde_stat.save()
        
        return redirect(request.session['previous_url'])
    return redirect('orders_list_designer',id)

def designer_section(request):
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
   
    orde=orders_crm.objects.filter(stage="designing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="designing").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']="home/pending_payment.html"

    context={
            'segment':segment,
            'stg':"Designing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/designer_section.html',context)


def filter_designing_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="order_managements"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="designing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="designing")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Designing orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/designer_section.html', context)


def filter_designing_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="designing" )
        ord_item=checkout_item_crm.objects.all()
        segment="order_managements"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="designing" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Designing orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/designer_section.html', context)



#####!*/**/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/* For Cutting - Admin


def cutting_section(request):
   
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
   
    orde=orders_crm.objects.filter(stage="cutting").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="cutting").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']="home/pending_payment.html"

    context={
            'segment':segment,
            'stg':"Cutting Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/cutting_section.html',context)



def filter_cutting_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="order_managements"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="cutting")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="cutting")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Cutting orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/cutting_section.html', context)


def filter_cutting_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="cutting" )
        ord_item=checkout_item_crm.objects.all()
        segment="order_managements"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="cutting" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Cutting orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/cutting_section.html', context)


def stiching_section(request):
   
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
   
    orde=orders_crm.objects.filter(stage="stiching").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="stiching").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']="home/cutting_section.html"

    context={
            'segment':segment,
            'stg':"Stiching Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/stiching_section.html',context)

def filter_stiching_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="order_managements"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="stiching")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="stiching")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Stiching orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/stiching_section.html', context)


def filter_stiching_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="stiching" )
        ord_item=checkout_item_crm.objects.all()
        segment="order_managements"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="stiching" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Stiching orders",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/stiching_section.html', context)



def printing_section(request):
   
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
   
    orde=orders_crm.objects.filter(stage="printing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="printing").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']="home/pending_payment.html"

    context={
            'segment':segment,
            'stg':"Printing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/printing_section.html',context)

def filter_printing_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="order_managements"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="printing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="printing")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Printing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/printing_section.html', context)


def filter_printing_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="printing" )
        ord_item=checkout_item_crm.objects.all()
        segment="order_managements"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="printing" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Printing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/printing_section.html', context)




def testing_section(request):
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
   
    orde=orders_crm.objects.filter(stage="testing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="testing").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']="home/pending_payment.html"

    context={
            'segment':segment,
            'stg':"Testing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/testing_section.html',context)

def filter_testing_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="order_managements"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="testing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="testing")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Testing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/testing_section.html', context)


def filter_testing_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="testing" )
        ord_item=checkout_item_crm.objects.all()
        segment="order_managements"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="testing" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Testing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/testing_section.html', context)

def packing_section(request):
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
   
    orde=orders_crm.objects.filter(stage="packing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="packing").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']="home/pending_payment.html"

    context={
            'segment':segment,
            'stg':"Packing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/packing_section.html',context)


def filter_packing_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="order_managements"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="packing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="packing")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Packing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/packing_section.html', context)


def filter_packing_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="packing" )
        ord_item=checkout_item_crm.objects.all()
        segment="order_managements"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="packing" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Packing Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/packing_section.html', context)


def despatch_section(request):
    resolved_func = resolve(request.path_info).func
    segment="order_managements"
   
    orde=orders_crm.objects.filter(stage="despatch").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="despatch").order_by("-id")
    ord_item_client=checkout_item.objects.all()
    request.session['previous_html']="home/pending_payment.html"

    context={
            'segment':segment,
            'stg':"Despatch Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
    
    return render(request, 'home/despatch_section.html',context)


def filter_despatch_orders(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="order_managements"
       
        orde = orders_crm.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="despatch")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(date__gte=st_dt,date__lte=en_dt,stage="despatch")
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Despatch Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/despatch_section.html', context)


def filter_despatch_orders_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="despatch" )
        ord_item=checkout_item_crm.objects.all()
        segment="order_managements"
    
        orde_client=orders.objects.filter(regno=ord_id,stage="despatch" )
        ord_item_client=checkout_item.objects.all()
        context={
            'segment':segment,
            'stg':"Despatch Section",
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
        }
        return render(request,'home/despatch_section.html', context)

############################################################  STAFF MODULE

def staff_index(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__
    usr=request.session['userid']
    userss=user_registration.objects.get(id=usr)
    data = item.objects.all()
    sub_cat=sub_category.objects.all()
    today = datetime.now()
    sub=orders.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
    event=events.objects.filter(start__date=date.today())

    nm=[]
    cnt=[]
    for i in sub:
        
        nm.append(i)
        qty=orders.objects.filter(date__day=i).count()
        cnt.append(qty)

    sub2=orders_crm.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
    for i in sub2:
        
        nm.append(i)
        qty=orders.objects.filter(date__day=i).count()
        cnt.append(qty)
    
 
    return render(request,"staff/staff_index.html",{'segment':segment,"user":userss,'sub_cat':sub_cat,'nm':nm,'cnt':cnt,'data': data,'event':event})


def filter_date_event_staff(request):
    if request.method=="POST":
        dates=request.POST.get('date_filter',None)
        segment="dashboard"
        try:
            usr=request.session['userid']
            user=user_registration.objects.get(id=usr)
        except:
            user=None
        data = item.objects.all()
        sub_cat=sub_category.objects.all()
        today = datetime.now()
        sub=orders.objects.filter(date__month=today.month).values_list('date__day', flat=True).distinct()
        event=events.objects.filter(start=dates)

        nm=[]
        cnt=[]
        for i in sub:
            
            nm.append(i)
            qty=orders.objects.filter(date__day=i).count()
            cnt.append(qty)

        
    
        return render(request,'home/staff_index.html',{'segment':segment,"user":user,'sub_cat':sub_cat,'nm':nm,
            'cnt':cnt,'data': data,'event':event})
    return redirect('dashboard')



def profile(request):
    ids=request.session['userid']
    usr=user_registration.objects.get(id=ids)
    
    context={
        'pro':usr,
        'user':usr,
    }
    return render(request, 'staff/profile.html',context)

def edit_user_profile(request,id):
    if request.method == "POST":
        form = user_registration.objects.get(id=id)
        eml=form.email
      
        form.name = request.POST.get('name',None)

        form.dob = request.POST.get('date_of_birth',None)
        form.number = request.POST.get('phone_number',None)
        form.email = request.POST.get('email',None)
        if request.FILES.get('image',None) == None:
            pass
        else:
            form.profile = request.FILES.get('image',None)
        form.addres = request.POST.get('address',None)
        form.location = request.POST.get('location')
        if request.POST.get('password',None) == "":
            form.password == form.password
        else:
            if request.POST.get('password',None) == request.POST.get('con_password',None):
                form.password == request.POST.get('password',None)
            else:
                messages.error(request,"Passwords do not match!")
                return redirect ("profile")
       
        form.save()
   
        
        return redirect ("profile")
    return redirect ("profile")


#***********/*/*/*/*/*/*/*/***********************  Designer Section
def order_staff_designer(request):
  
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.filter(stage="designing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="designing").order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="working")
    
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/order_staff_designer.html',context)

def staff_filter_order_design(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="orders_dta"

        resolved_func = resolve(request.path_info).func
        segment="order_staff_designer"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="designing")
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="designing")
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="working")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/order_staff_designer.html', context)


def staff_filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="designing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,stage="designing")
        ord_item_client=checkout_item.objects.all()
        segment="order_staff_designer"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="working")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/order_staff_designer.html', context)



def staff_orders_list_designer(request,id):
    orde = orders_crm.objects.filter(id=id).order_by("-id")
    ord_item=checkout_item_crm.objects.filter(orders=id)

    segment="order_staff_designer"
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
 
    context={
        "orders":orde,
        "ord_item":ord_item,
        'segment':segment,
        'user':user,
    
    }
    return render(request, 'staff/staff_orders_list_client.html', context)

def staff_orders_list_designer_client(request,id):
    orde = orders.objects.filter(id=id).order_by("-id")
   
    ord_item=checkout_item.objects.filter(id=id)
    
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    segment="order_staff_designer"
  
    orde_stat = orders.objects.get(id=id)

    context={
        "orders":orde,
        "ord_item":ord_item,
        'segment':segment,
 
        'ord_ids':id,
        'orde_stat':orde_stat,
        'user':user,
    }
    return render(request, 'staff/staff_orders_list_designer_client.html', context)

def staff_change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')

    itm=orders_crm.objects.get(id=ele)
    itm.stage="payment"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def staff_change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')
 
    itm=orders.objects.get(id=ele)
    itm.stage="payment"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def completed_work_designer(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="completed")
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/completed_work_designer.html',context)


def staff_filter_complete_design(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
        segment="orders_dta"

        resolved_func = resolve(request.path_info).func
        segment="order_staff_designer"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="completed")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/completed_work_designer.html', context)


def staff_filter_complete_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="order_staff_designer"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="completed")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/completed_work_designer.html', context)


#***********/*/*/*/*/*/*/*/***********************  Cutting Section

def cutting_order_list(request):

    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.filter(stage="cutting").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="cutting").order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="working")
    
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/cutting_order_list.html',context)


def cutting_filter_order_date(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
      

        resolved_func = resolve(request.path_info).func
        segment="cutting_order_list"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="cutting")
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="cutting")
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="working")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/cutting_order_list.html', context)


def cutting_filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="cutting")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,stage="cutting")
        ord_item_client=checkout_item.objects.all()
        segment="cutting_order_list"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="working")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/cutting_order_list.html', context)




def cutting_complete_order(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="completed")
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/cutting_complete_order.html',context)


def cutting_filter_complete_order(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')


        resolved_func = resolve(request.path_info).func
        segment="cutting_completed_work"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="completed")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/cutting_complete_order.html', context)


def cutting_filter_complete_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="cutting_completed_work"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="completed")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/cutting_complete_order.html', context)


def cutting_change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')

    itm=orders_crm.objects.get(id=ele)
    itm.stage="stiching"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def cutting_change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')
 
    itm=orders.objects.get(id=ele)
    itm.stage="stiching"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


#! Stiching Section
def stiching_order_list(request):

    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.filter(stage="stiching").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="stiching").order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="working")
    
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/stiching_order_list.html',context)


def stiching_filter_order_date(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
      

        resolved_func = resolve(request.path_info).func
        segment="stiching_order_list"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="stiching")
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="stiching")
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="working")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/stiching_order_list.html', context)


def stiching_filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="stiching")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,stage="stiching")
        ord_item_client=checkout_item.objects.all()
        segment="stiching_order_list"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="working")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/stiching_order_list.html', context)




def stiching_complete_order(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="completed")
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/stiching_complete_order.html',context)


def stiching_filter_complete_order(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')


        resolved_func = resolve(request.path_info).func
        segment="stiching_complete_order"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="completed")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/stiching_complete_order.html', context)


def stiching_filter_complete_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="stiching_complete_order"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="completed")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/stiching_complete_order.html', context)

def stiching_change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')

    itm=orders_crm.objects.get(id=ele)
    itm.stage="printing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def stiching_change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')
 
    itm=orders.objects.get(id=ele)
    itm.stage="printing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


# ? ----------------------------------------------------------------------printning section

def printing_order_list(request):

    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.filter(stage="printing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="printing").order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="working")
    
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/printing_order_list.html',context)


def printing_filter_order_date(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
      

        resolved_func = resolve(request.path_info).func
        segment="printing_order_list"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="printing")
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="printing")
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="working")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/printing_order_list.html', context)


def printing_filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="printing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,stage="printing")
        ord_item_client=checkout_item.objects.all()
        segment="printing_order_list"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="working")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/printing_order_list.html', context)




def printing_complete_order(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="completed")
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/printing_complete_order.html',context)


def printing_filter_complete_order(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')


        resolved_func = resolve(request.path_info).func
        segment="printing_complete_order"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="completed")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/printing_complete_order.html', context)


def printing_filter_complete_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="printing_complete_order"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="completed")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/printing_complete_order.html', context)



def printing_change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')

    itm=orders_crm.objects.get(id=ele)
    itm.stage="testing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def printing_change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')
 
    itm=orders.objects.get(id=ele)
    itm.stage="testing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


#!------------------------------------------------------------------ TESTING AREA

def testing_order_list(request):

    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.filter(stage="testing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="testing").order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="working")
    
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/testing_order_list.html',context)


def testing_filter_order_date(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
      

        resolved_func = resolve(request.path_info).func
        segment="testing_order_list"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="testing")
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="testing")
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="working")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/testing_order_list.html', context)


def testing_filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="testing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,stage="testing")
        ord_item_client=checkout_item.objects.all()
        segment="testing_order_list"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="working")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/testing_order_list.html', context)




def testing_complete_order(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="completed")
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/testing_complete_order.html',context)


def testing_filter_complete_order(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')


        resolved_func = resolve(request.path_info).func
        segment="testing_complete_order"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="completed")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/testing_complete_order.html', context)


def testing_filter_complete_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="testing_complete_order"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="completed")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/testing_complete_order.html', context)



def testing_change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')

    itm=orders_crm.objects.get(id=ele)
    itm.stage="packing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def testing_change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')
 
    itm=orders.objects.get(id=ele)
    itm.stage="packing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})

#!------------------------------------------------------------------ packing AREA

def packing_order_list(request):

    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.filter(stage="packing").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="packing").order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="working")
    
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/packing_order_list.html',context)


def packing_filter_order_date(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
      

        resolved_func = resolve(request.path_info).func
        segment="packing_order_list"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="packing")
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="packing")
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="working")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/packing_order_list.html', context)


def packing_filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="packing")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,stage="packing")
        ord_item_client=checkout_item.objects.all()
        segment="packing_order_list"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="working")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/packing_order_list.html', context)




def packing_complete_order(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="completed")
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/packing_complete_order.html',context)


def packing_filter_complete_order(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')


        resolved_func = resolve(request.path_info).func
        segment="packing_complete_order"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="completed")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/packing_complete_order.html', context)


def packing_filter_complete_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="packing_complete_order"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="completed")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/packing_complete_order.html', context)



def packing_change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')

    itm=orders_crm.objects.get(id=ele)
    itm.stage="despatch"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def packing_change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')
 
    itm=orders.objects.get(id=ele)
    itm.stage="despatch"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})

#!------------------------------------------------------------------ despatch AREA

def despatch_order_list(request):

    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.filter(stage="despatch").order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.filter(stage="despatch").order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="working")
    
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/despatch_order_list.html',context)


def despatch_filter_order_date(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')
      

        resolved_func = resolve(request.path_info).func
        segment="despatch_order_list"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="despatch")
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt,stage="despatch")
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="working")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/despatch_order_list.html', context)


def despatch_filter_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id,stage="despatch")
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id,stage="despatch")
        ord_item_client=checkout_item.objects.all()
        segment="despatch_order_list"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="working")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/despatch_order_list.html', context)




def despatch_complete_order(request):
    resolved_func = resolve(request.path_info).func
    segment=resolved_func.__name__

    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
   
    orde=orders_crm.objects.all().order_by("-id")
    ord_item=checkout_item_crm.objects.all()

    orde_client=orders.objects.all().order_by("-id")
    ord_item_client=checkout_item.objects.all()

    assigns=order_management.objects.filter(user=user, work_status="completed")
 
    context={
            'segment':segment,
            'user':user,
            "orders":orde,
            "ord_item":ord_item,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
    
    return render(request, 'staff/despatch_complete_order.html',context)


def despatch_filter_complete_order(request):
    if request.method=="POST":
        st_dt=request.POST.get('str_dt')
        en_dt=request.POST.get('end_dt')


        resolved_func = resolve(request.path_info).func
        segment="despatch_complete_order"

        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
    
        orde = orders_crm.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item=checkout_item_crm.objects.all()

        orde_client=orders.objects.filter(date__date__gte=st_dt,date__date__lte=en_dt)
        ord_item_client=checkout_item.objects.all()

        assigns=order_management.objects.filter(user=user, work_status="completed")
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'assigns':assigns,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'user':user,
        }
        return render(request,'staff/despatch_complete_order.html', context)


def despatch_filter_complete_order_id(request):
    if request.method=="POST":
        ord_id=request.POST.get('ord_id')
        orde = orders_crm.objects.filter(regno=ord_id)
        ord_item=checkout_item_crm.objects.all()
        orde_client=orders.objects.filter(regno=ord_id)
        ord_item_client=checkout_item.objects.all()
        segment="despatch_complete_order"
        usr=request.session['userid']
        user=user_registration.objects.get(id=usr)
        assigns=order_management.objects.filter(user=user, work_status="completed")
  

        
        context={
            "orders":orde,
            "ord_item":ord_item,
            'segment':segment,
            'user':user,
            'orde_client':orde_client,
            'ord_item_client':ord_item_client,
            'assigns':assigns,
        }
        return render(request,'staff/despatch_complete_order.html', context)



def despatch_change_order_stage(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')

    itm=orders_crm.objects.get(id=ele)
    itm.stage="packing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})


def despatch_change_order_stage_client(request):
    ele = request.GET.get('ele')
    stg = request.GET.get('stage')
    mang_id = request.GET.get('mang_ids')
 
    itm=orders.objects.get(id=ele)
    itm.stage="packing"
    itm.save()
    mangement=order_management.objects.get(id=mang_id)

    # Sample date-time strings
    date_str1 = mangement.start_time
    date_str2 = timezone.now()

    # Calculate the difference
    time_difference = date_str1 - date_str2

    mangement.work_status=stg
    mangement.end_time=datetime.now()
    mangement.time_taken=time_difference
    mangement.save()
    usr=request.session['userid']
    user=user_registration.objects.get(id=usr)
    if user.preformance:
        user.preformance=int(user.preformance)+1
    else:
        user.preformance=1
    user.save()
    return JsonResponse({"status":" not"})



#main
def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')


###############################################################  Automatic Assigning

# staff status 
def auto_assign_function():
    print("sdfsfsfdsfsf"+str(timezone.now()))
    stf= user_registration.objects.filter(status="active")
    ord_manag=order_management.objects.all()
    ord_crm=orders_crm.objects.all()
    ord_client=orders.objects.all()
    for cli in ord_client:
        ord_ids=cli.id
        if (cli.stage == "pending") and (cli.status == "checkout"): 
           cli.stage="cutting"
           cli.save() 
            
        elif cli.stage == "designing":
            
            
            if order_management.objects.filter(order_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "designing":
                        if order_management.objects.filter(user=stf_id,work_status="completed").all().exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                          
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "cutting":
            
            
            if order_management.objects.filter(order_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "cutting":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "stiching":
            
            
            if order_management.objects.filter(order_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "stiching":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "printing":
            
            if order_management.objects.filter(order_id=ord_ids).exists():
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "printing":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "testing":
            
            if order_management.objects.filter(order_id=ord_ids).exists():
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "testing":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "packing":
            
            if order_management.objects.filter(order_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "packing":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "despatch":
            
            if order_management.objects.filter(order_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "despatch":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=cli.id
                            ord_ass.order_crm_id=None
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                       
        else:
            pass

    #?order crm section

    for cli in ord_crm:
      
        ord_ids=cli.id
      
        if (cli.stage == "pending") and (cli.status == "checkout"): 
           cli.stage="cutting"
           cli.save() 
            
        elif cli.stage == "designing":
            
            
            if order_management.objects.filter(order_crm_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "designing":
                        
                        if order_management.objects.filter(user=stf_id,work_status="completed", order_id=None, order_crm_id=cli.id).exists():
                            print("working if condition")
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            print("working this stage")
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "cutting":
            
            
            if order_management.objects.filter(order_crm_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "cutting":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ordord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id                          
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "stiching":
            
            
            if order_management.objects.filter(order_crm_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "stiching":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "printing":
            
            if order_management.objects.filter(order_crm_id=ord_ids).exists():
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "printing":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "testing":
            
            if order_management.objects.filter(order_crm_id=ord_ids).exists():
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "testing":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "packing":
            
            if order_management.objects.filter(order_crm_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "packing":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        elif cli.stage == "despatch":
            
            if order_management.objects.filter(order_crm_id=ord_ids).exists():
                
                pass
            else:
                
                
                for stf_id in stf:
                    
                    if stf_id.designation == "despatch":
                        if order_management.objects.filter(user=stf_id,work_status="completed").exists():
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                        elif order_management.objects.filter(user=stf_id,work_status="working").exists():
                            pass
                        else:
                            ord_ass=order_management()
                            ord_ass.user=stf_id
                            ord_ass.order_id=None
                            ord_ass.order_crm_id=cli.id
                            ord_ass.work_status="working"
                            ord_ass.start_time=timezone.now()
                            ord_ass.order_no=cli.regno
                            ord_ass.save()
                    else:
                        pass
        else:
            pass


def run_function_every_10_minutes():
   
    while True:
        auto_assign_function()
        time.sleep(60)  # 600 seconds = 10 minutes

# Create a separate thread to run the function
thread = threading.Thread(target=run_function_every_10_minutes)

# Start the thread
thread.start()

    # Add your other tasks or logic here
