from django import template
from hiring.models import *
from django.template import Library

register = Library()

def next(value,i):
	obj1 = Test.objects.get(id=value)
	obj2 = obj1.question.all()
	for j,t in enumerate(obj2):
		if t.id == i:
			try:
				obj3 = obj2[j+1]
				return obj3.id
			except:
				return i

def previous(value,i):
	obj1 = Test.objects.get(id=value)
	obj2 = obj1.question.all()
	for j,t in enumerate(obj2):
		if t.id == i:
			try:
				obj3 = obj2[j-1]
				return obj3.id
			except:
				return i
register.filter('next',next)
register.filter('previous',previous)