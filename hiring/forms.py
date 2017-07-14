from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from  .models import *
from django.contrib.auth import authenticate


class UserCreationForm(UserCreationForm):
	email=forms.EmailField(required=True)

	class Meta:
		model=User
		fields=['username','email','password1','password2']

	def clean_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			raise forms.ValidationError("This email already exists.")
		return data

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user	
class Userform(forms.ModelForm):
	class Meta:
		model=Profile
		exclude=('user','email','height','width')
		widgets = {
            'dob': forms.widgets.DateInput(attrs={'type': 'dob'}),
            }
class Loginform(forms.Form):
	username=forms.CharField(required=True)
	password=forms.CharField(widget=forms.PasswordInput)

	def clean(self,*args,**kwargs):
		username=self.cleaned_data.get('username')
		password=self.cleaned_data.get('password')
		user=authenticate(username=username,password=password)
		if username and password:
			if not user:
				raise forms.ValidationError("User doesn't exists")
			if not user.check_password(password):
				raise forms.ValidationError("password is incorrect")
			if not user.is_active:
				raise forms.ValidationError('User is not active')
			return super(Loginform,self).clean(*args,**kwargs)
class Eventform(forms.ModelForm):
	class Meta:
		model=Events
		fields=['name','desc']