from django.contrib import admin

# Register your models here.
from .models import Question, Topic, Point, Message, CorrectAnswer, Profile
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Point)
admin.site.register(Message)
admin.site.register(CorrectAnswer)
admin.site.register(Profile)

