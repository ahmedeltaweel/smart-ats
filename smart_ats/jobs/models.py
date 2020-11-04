from django.db import models
from smart_ats.companies.models import *
from taggit.managers import TaggableManager
# Create your models here.

class Tag(models.Model):
    #name=models.CharField(max_length = 200,null=True)
    name=TaggableManager();

class Category(models.Model):
    title =models.CharField(max_length = 200,null=True)


class Job(models.Model):
	STATUS=(
		('Active','Active'),
		('Draft','Draft'),
		('Archived','Archived'),
		)
	title=models.CharField(max_length = 200,null=True)
	description=models.CharField(max_length = 200,null=True,blank=True)
	category_id=models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
	company_id=models.ForeignKey(Company,null=True,on_delete=models.SET_NULL)
	Author_id=models.ForeignKey(CompanyAdmin,null=True,on_delete=models.SET_NULL)
	status=models.CharField(max_length = 200, null=True, choices=STATUS)
	tags=models.ManyToManyField("Tag")
	def __str__(self):
		return self.name 

