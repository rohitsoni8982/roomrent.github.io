from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings

from mydjproject import models as mydjproject_models
from myadmin import models as myadmin_models
MEDIA_URL=settings.MEDIA_URL

#middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=='/user/searchproperty/' or request.path=='/user/searchsubcategory/' :
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

# Create your views here.
def userhome(request):
 return render(request,"userhome.html",{"sunm":request.session["sunm"]})     

def searchproperty(request):
 clist=myadmin_models.Category.objects.all()    
 return render(request,"searchproperty.html",{"clist":clist,"MEDIA_URL":MEDIA_URL,"sunm":request.session["sunm"]})

def searchsubcategory(request):
 cnm=request.GET.get("cnm")     
 clist=myadmin_models.Category.objects.all()
 sclist=myadmin_models.SubCategory.objects.filter(catname=cnm)    
 return render(request,"searchsubcategory.html",{"cnm":cnm,"clist":clist,"sclist":sclist,"MEDIA_URL":MEDIA_URL,"sunm":request.session["sunm"]})     

def viewproperty(request):
 cnm=request.GET.get("cnm")
 scnm=request.GET.get("scnm")
 sclist=myadmin_models.SubCategory.objects.filter(catname=cnm)
 plist=myadmin_models.Product.objects.filter(catname=cnm,subcatname=scnm)
 return render(request,"viewproperty.html",{"cnm":cnm,"scnm":scnm,"sclist":sclist,"plist":plist,"MEDIA_URL":MEDIA_URL,"sunm":request.session["sunm"]})

def epuser(request):
 sunm=request.session["sunm"]  	
 userDetails=mydjproject_models.Register.objects.filter(email=sunm)
 m,f="",""
 if userDetails[0].gender=="male":
  m="checked"
 else:
  f="checked"	   	  
 #print(userDetails[0])
 if request.method=="GET":	
  return render(request,"epuser.html",{"sunm":sunm,"userDetails":userDetails[0],"m":m,"f":f})
 else:
  name=request.POST.get("name")
  email=request.POST.get("email")	  
  mobile=request.POST.get("mobile")
  address=request.POST.get("address")
  city=request.POST.get("city")
  gender=request.POST.get("gender")

  mydjproject_models.Register.objects.filter(email=email).update(name=name,mobile=mobile,address=address,gender=gender,city=city)
  
  return redirect("/user/epuser/")	    


def cpuser(request):
 sunm=request.session["sunm"]
 if request.method=="GET":	
  return render(request,"cpuser.html",{"sunm":sunm,"output":""})
 else:
  opass=request.POST.get("opass")
  npass=request.POST.get("npass")	 
  cnpass=request.POST.get("cnpass")
  
  userDetails=mydjproject_models.Register.objects.filter(email=sunm,password=opass)
  
  if len(userDetails)>0:
   if npass==cnpass:
    mydjproject_models.Register.objects.filter(email=sunm).update(password=cnpass)	   
    msg="Password changed successfully , please login again...."
   else:
    msg="New & confirm new password mismatch"	   	   
  else:
   msg="Invalid old password"	  	  

  return render(request,"cpuser.html",{"sunm":sunm,"output":msg})  	   		  