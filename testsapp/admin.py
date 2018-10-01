from django.contrib import admin
from .models import TestGroup, Test, Question, Answer

# Register your models here.
admin.site.register(TestGroup)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
