from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from mydjproject import models as mydjproject_models
from . import models
import time

#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/' :
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

# Create your views here.
def adminhome(request):
 return render(request,"adminhome.html",{"sunm":request.session["sunm"]})

def addproperty(request):
 clist=models.Category.objects.all()
 if request.method=="GET":   
  return render(request,"addproperty.html",{"sunm":request.session["sunm"],"output":"","clist":clist})
 else:
  title=request.POST.get("title")
  catname=request.POST.get("catname")
  subcatname=request.POST.get("subcatname")
  description=request.POST.get("description")
  locality=request.POST.get("locality")
  city=request.POST.get("city")
  info=time.asctime()
  picon=request.FILES["picon"]
  fs = FileSystemStorage()
  filename = fs.save(picon.name,picon)
  p=models.Product(title=title,catname=catname,subcatname=subcatname,description=description,locality=locality,city=city,piconname=filename,info=info)
  p.save()     
  return render(request,"addproperty.html",{"sunm":request.session["sunm"],"output":"Property added successfully....","clist":clist})     

def manageoptions(request): 
 return render(request,"manageoptionlinks.html",{"sunm":request.session["sunm"]})
 
def manageusers(request):
 userDetails=mydjproject_models.Register.objects.filter(role="user")
 #print(userDetails)    
 return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})      

def manageuserstatus(request):
 regid=int(request.GET.get("regid"))    
 s=request.GET.get("s")
 if s=="block":
  mydjproject_models.Register.objects.filter(regid=regid).update(status=0)
 elif s=="verify":
  mydjproject_models.Register.objects.filter(regid=regid).update(status=1)
 else:
  mydjproject_models.Register.objects.filter(regid=regid).delete()               
 return redirect("/myadmin/manageusers/")     

def addcategory(request):
 if request.method=="GET":    
  return render(request,"addcategory.html",{"output":"","sunm":request.session["sunm"]})
 else:
  catname=request.POST.get("catname")
  caticon=request.FILES["caticon"]
  fs = FileSystemStorage()
  filename = fs.save(caticon.name,caticon)
  #print(filename+"-----"+catname)
  p=models.Category(catname=catname,caticonname=filename)
  p.save()     
  return render(request,"addcategory.html",{"output":"Category Added Successfully....","sunm":request.session["sunm"]})

def fetchSubCatAJAX(request):
  catname=request.GET.get("catname");  
  sclist=models.SubCategory.objects.filter(catname=catname)
  optionlist="<option>Select Sub Category</option>"
  for row in sclist:
    optionlist+=("<option>"+row.subcatname+"</option>")
  return HttpResponse(optionlist)

def addsubcategory(request):
 clist=models.Category.objects.all() 
 if request.method=="GET":    
  return render(request,"addsubcategory.html",{"output":"","clist":clist,"sunm":request.session["sunm"]})
 else:
  catname=request.POST.get("catname")
  subcatname=request.POST.get("subcatname")
  caticon=request.FILES["caticon"]
  fs = FileSystemStorage()
  filename = fs.save(caticon.name,caticon)
  #print(filename+"-----"+catname)
  p=models.SubCategory(catname=catname,subcatname=subcatname,subcaticonname=filename)
  p.save()     
  return render(request,"addsubcategory.html",{"output":"SubCategory Added Successfully....","clist":clist,"sunm":request.session["sunm"]})           