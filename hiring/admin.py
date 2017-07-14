from django.contrib import admin
from .models import Events,Datetime,Questions,Answer,Test



 
admin.site.site_header = 'Startxlabs Hiring Portal'
admin.site.site_title = 'Startxlabs Hiring Portal'
admin.site.index_title = 'Startxlabs Hiring Portal'

class DateInline(admin.StackedInline):
	model=Datetime
	extra=0
class EventsAdmin(admin.ModelAdmin):
	inlines=[
	DateInline,
	]
class AnswerInline(admin.StackedInline):
	model=Answer
	extra=0
class QuestionsAdmin(admin.ModelAdmin):
	inlines=[
	AnswerInline,
	]
admin.site.register(Questions,QuestionsAdmin)	
admin.site.register(Events,EventsAdmin)
admin.site.register(Test)
