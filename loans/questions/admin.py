from django.contrib import admin

# profiles
from .models import (Choice, Question)


class QuestionAdmin(admin.ModelAdmin):
    pass

class ChoiceAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)