from django.db import models
from django.contrib.auth.models import User


def upload_image(instance,filename):
	return "cv/%s/%s"%(instance.id,filename)

def uploadcv(instance,filename):
	return "cv/%s/%s"%(instance.id,filename)

class Profile(models.Model):
	m='male'
	f='female'
	gender=((m,'male'),
		(f,'female'))
	user= models.OneToOneField(User,related_name='profile')
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	dob=models.DateField(auto_now=False,auto_now_add=False)
	gender=models.CharField(max_length=15,choices=gender)
	photo=models.ImageField(upload_to=upload_image,null=True,height_field='height', width_field='width',blank=True)
	height=models.IntegerField(default=0)
	width=models.IntegerField(default=0)
	skills=models.TextField()
	cv=models.FileField(upload_to=uploadcv,null=True,blank=True)
	def __str__(self):
		return self.first_name+" "+self.last_name

class Token(models.Model):
	user=models.OneToOneField(User,related_name='token')
	token=models.CharField(max_length=300,null=True)


class Events(models.Model):
	i='Internship'
	f='Full-Time'
	p='Part-Time'
	job_type=((i,'Internship'),(f,'Full-Time'),(p,'Part-Time'))
	posted_on=models.DateField(auto_now=False, auto_now_add=True)
	name=models.CharField(max_length=100,verbose_name="Event Name")
	type_job=models.CharField(max_length=20,choices=job_type)
	vacancies=models.IntegerField(default=0)
	desc=models.TextField()
	time_duration=models.IntegerField(default=0)
	salary=models.CharField(max_length=50,default='Based on performance')
	end_date=models.DateField(auto_now=False, auto_now_add=False)
	def __str__(self):
		return self.name



class Datetime(models.Model):
	event=models.ForeignKey(Events,on_delete=models.CASCADE,related_name='date')
	date=models.DateField(auto_now=False, auto_now_add=False)
	time=models.TimeField(auto_now=False, auto_now_add=False)

class Exam(models.Model):
	profile=models.ForeignKey(Profile)
	event=models.ForeignKey(Events,on_delete=models.CASCADE)
	start_date=models.DateField(auto_now=False, auto_now_add=False)
	start_time=models.TimeField(auto_now=False, auto_now_add=False)
	registered=models.BooleanField(default=False)

def upload(instance,filename):
	return "files/"
class Test(models.Model):
	category=models.CharField(max_length=100)
	answer_files=models.FileField(blank=True)
	def __str__(self):
		return self.category

class Questions(models.Model):
	test=models.ForeignKey(Test,related_name='question')
	question=models.TextField()
	subjective=models.BooleanField(default=False)
	cc=models.CharField(max_length=10,blank=True)
	def __str__(self):
		return self.question

class Answer(models.Model):
	question=models.ForeignKey(Questions,related_name='answers')
	choice=models.CharField(max_length=300,blank=True)
	text=models.TextField(blank=True)
	





