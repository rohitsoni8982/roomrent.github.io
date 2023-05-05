from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import models
from . import emailAPI
import time

#middleware to check session for mainapp routes
def sessioncheck_middleware(get_response):
	def middleware(request):
		if request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
			request.session['sunm']=None
			request.session['srole']=None
			response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

def home(request):
 return render(request,"home.html")

def about(request):
 return render(request,"about.html")

def contact(request):
 return render(request,"contact.html")

def service(request):
 return render(request,"service.html")

def register(request):
 if request.method=="GET":     
  return render(request,"register.html",{"output":""})
 else:
  #to recieve data from post method
  #print(request.POST)
  name=request.POST.get("name")
  email=request.POST.get("email")
  password=request.POST.get("password")
  mobile=request.POST.get("mobile")
  address=request.POST.get("address")
  city=request.POST.get("city")
  gender=request.POST.get("gender")
  info=time.asctime()

  #to send verification email
  emailAPI.sendMail(email,password)

  #to insert record in database
  p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=info)              
  p.save()

  return render(request,"register.html",{"output":"User register successfully...."})       

def verify(request):
  vemail=request.GET.get("vemail")
  models.Register.objects.filter(email=vemail).update(status=1)
  return redirect("/login/")  

def checkEmailAvaibility(request):
  emailid=request.GET.get("emailid")
  userDetails=models.Register.objects.filter(email__startswith=emailid)
  if len(userDetails)>0:
    return HttpResponse(1)
  else:      
    return HttpResponse(0)
        
def login(request):
 cunm,cpass="",""
 if request.COOKIES.get("cunm")!=None:
  cunm=request.COOKIES.get("cunm")
  cpass=request.COOKIES.get("cpass") 

 if request.method=="GET":    
  return render(request,"login.html",{"cunm":cunm,"cpass":cpass,"output":""})
 else:
  #to get user details to make login
  email=request.POST.get("email")
  password=request.POST.get("password")

  #to match user details in database
  userDetails=models.Register.objects.filter(email=email,password=password,status=1)            

  #to check valid user login
  if len(userDetails)>0:

   #to set user details in session
   request.session["sunm"]=userDetails[0].email
   request.session["srole"]=userDetails[0].role

   if userDetails[0].role=="admin":   
    response=redirect("/myadmin/")
   else:
    response=redirect("/user/")

   #to store user details in cookies
   chk=request.POST.get("chk")
   if(chk!=None):
    response.set_cookie("cunm",userDetails[0].email,max_age=3600*24*365)    
    response.set_cookie("cpass",userDetails[0].password,max_age=3600*24*365)
  
   return response           

  else:
   return render(request,"login.html",{"output":"Invalid user or verify your account....","cunm":cunm,"cpass":cpass})
