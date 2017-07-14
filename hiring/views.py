from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from django.core.mail import send_mail
from base64 import b64encode
from os import urandom
from .models import *
from .forms import *
from django.views.generic import DetailView
from django.http import HttpResponse
import  datetime
from django.core.files.base import ContentFile
from random import randint
from django.core.files.base import ContentFile
from django.conf import settings



# Create your views here.
def home(request):
	title='startxlabs Recruitement Home'
	context={
	'title':title
	}
	return render(request,'hiring/home.html',context)

def signup(request):
	title='Signup Page'
	if request.user.is_active:
		logout(request)

	user_form = UserCreationForm()

	if request.method == 'POST':
		user_form = UserCreationForm(request.POST)
		if user_form.is_valid():
				u = user_form.save(commit=False)
				u.is_active = False
				u.save()
				random_bytes = urandom(25)
				token = b64encode(random_bytes).decode('utf-8')
				tokenobj=Token.objects.create(user_id=u.id)
				tokenobj.token=token
				tokenobj.save()
				subject = "Email Verification"
				email=user_form.cleaned_data.get('email')
				message = "Please click on this link to verify your email address : \" http://127.0.0.1:8000/hiring/afterverification/%s \" " %(token)
				recipient_list = [email]
				from_email = 'startxlabstestuser@gmail.com'
				send_mail(subject,message,from_email,recipient_list)
				return redirect('/hiring/emailsent/')	
		# print vars(user_form)
	context={
	'title':title,
	'user_form':user_form,

	}
	return render(request,'hiring/signup.html',context)


def afterverify(request,token):
	title='Email Verification'
	try:
		usernow = Token.objects.get(token=token)
	except User.DoesNotExist:
		error(request,"Invalid user.Please check the link again.")
		return redirect('hiring:home')
	usernew = User.objects.get(id=usernow.user.id)
	form = Userform()
	if request.method =='POST':
		form=Userform(request.POST ,request.FILES)
		if form.is_valid():
			u=form.save(commit=False)
			first=form.cleaned_data.get('first_name')
			last=form.cleaned_data.get('last_name')
			dob=form.cleaned_data.get('dob')
			gender=form.cleaned_data.get('gender')
			image=form.cleaned_data.get('photo')
			cv=form.cleaned_data.get('cv')
			usernew.is_active=True
			usernew.save()
			usernow.applied = True
			usernow.delete()
			obj=Profile.objects.create(user_id=usernew.id,first_name=first,last_name=last,dob=dob,gender=gender,photo=image,cv=cv)
			return redirect('hiring:home')
			
	context={
	'title':title,
	'form':form

	}
	return render(request,'hiring/afterv.html',context)
def userlogin(request):
	title='Login page'
	form=Loginform(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(username=username,password=password)
		login(request,user)
		print (request.user.is_authenticated)
		return redirect('hiring:home')
	context={
	'title':title,
	'form':form
	}
	return render(request,'hiring/login.html',context)
def userlogout(request):
	logout(request)
	return render(request,'hiring/logout.html',{})

def showevents(request):
	title='Events'
	all_events=Events.objects.all()
	context={
	'title':title,
	'all_events':all_events
	}
	return render(request,'hiring/events.html',context)


def showevent(request,pk):
	event=Events.objects.get(pk=pk)
	title=event.name
	date = datetime.datetime.today().date()
	time = datetime.datetime.now().time()
	# print (time)
	delta=datetime.timedelta(minutes=event.time_duration)
	# print (delta)
	try:
		exam = Exam.objects.get(profile = request.user.profile,event=event)
		end_time=(datetime.datetime.combine(datetime.datetime.today().date(),exam.start_time)+delta).time()
		print time >= exam.start_time
		print end_time >= time
	except:
		exam=None
		end_time=datetime.datetime.now().time()
	context={
	'title':title,
	'events':event,
	'exam':exam,
	'date':date,
	'time':time,
	'end_time':end_time,
	}
	return render(request,'hiring/event.html',context)

@login_required(login_url='/hiring/login/')
def calenderview(request,pk):
	event=Events.objects.get(id=pk)
	date = Datetime.objects.filter(event__id = pk)
	profile=Profile.objects.get(user_id=request.user.id)

	context={
	'event':event,
	'date':date,
	'profile':profile,
	}
	return render(request,'hiring/calender.html',context)

@login_required(login_url='/hiring/login/')
def register(request,events_id,key,start_date,start_time):
	title='Register for the Event'
	profile=Profile.objects.get(id=key)
	event=Events.objects.get(id=events_id)
	name=event.name
	date=start_date
	time=start_time
	salary=event.salary	
	if request.method=='POST':
		exam=Exam.objects.create(profile=profile,event=event,start_date=start_date,start_time=start_time,registered=True)
		subject = "Email Verification"
		email=request.user.email
		message ="you have registered for the test"
		recipient_list = [email]
		from_email = 'startxlabstestuser@gmail.com'
		send_mail(subject,message,from_email,recipient_list)
		return redirect('hiring:home')
	context={
	'title':title,
	'name':name,
	'date':date,
	'time':time,
	'salary':salary,
	}		
	return render(request,'hiring/register.html',context)


@login_required(login_url='/hiring/login/')
def agree(request,pk):
	exam=Exam.objects.get(pk=pk)
	context={
	'exam':exam
	}
	return render(request,'hiring/agree.html',context)

@login_required(login_url='/hiring/login/')
def test(request,pk):
	exam=Exam.objects.get(pk=pk)
	name=exam.event.name
	test=Test.objects.filter(category=name)
	title="Test"
	i=randint(0,len(test)-1)
	questions=test[i]
	j=questions.pk
	k=questions.question.first().pk
	context={
	'qid':j,
	'questions':questions,
	'id':k,
	'title':title
	}
	return render(request,'hiring/test.html',context)

def question(request,pk):
	test=Test.objects.get(pk=pk)
	context={
	'test':test,
	}
	return render(request,'hiring/Questionframe.html',context)
import os
def solution(request,pk,testpk):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file_path = os.path.join(os.path.dirname(BASE_DIR),"media_cdn")
	obj=Test.objects.get(pk=testpk)
	question=Questions.objects.get(pk=pk)
	cat = '_'.join(obj.category.split())
	data = dict()
	if request.method == 'POST':
		old_text = ''
		print file_path+'/'+request.user.username+'/'+obj.category+'.txt'
		if os.path.exists(file_path+'/'+request.user.username+'/'+cat+'.txt'):
			with open(file_path+'/'+request.user.username+'/'+cat+'.txt', 'r') as file:
				old_text = file.read() + '\n'
				os.remove(file_path+'/'+request.user.username+'/'+cat+'.txt')
		data = request.POST.dict()
		try:
			print data.get('choice')
			text=question.question+" , "+data['choice']+" , "+question.cc
			content = ContentFile(old_text+text)
		except:
			text=question.question+" "+data['answer']
			content=ContentFile(old_text+text)
		obj.answer_files.save(file_path+'/'+request.user.username+'/'+cat+'.txt', content)
		obj.save()
	context={
	'question':question,
	'test':obj,
	'abc':obj.id,
	'data':data.get('choice') or data.get('answer')
	}
	return render(request,'hiring/solutionframe.html',context)



	

