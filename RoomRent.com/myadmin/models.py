from django.db import models

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=50,unique=True)
    caticonname=models.CharField(max_length=100)

class SubCategory(models.Model):
    subcatid=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=50)
    subcatname=models.CharField(max_length=50,unique=True)
    subcaticonname=models.CharField(max_length=100)

class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    catname=models.CharField(max_length=50)
    subcatname=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    locality=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    piconname=models.CharField(max_length=100) 
    info=models.CharField(max_length=50)       

    
