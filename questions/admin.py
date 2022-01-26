from django.contrib import admin
from .models import Question, CheckQues, CurrentQues
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Question, QuestionAdmin)

class CheckQuesAdmin(admin.ModelAdmin):
    pass
admin.site.register(CheckQues, CheckQuesAdmin)

class CurrentQuesAdmin(admin.ModelAdmin):
    pass
admin.site.register(CurrentQues, CurrentQuesAdmin)
