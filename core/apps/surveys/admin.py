from django.contrib import admin

from core.apps.surveys.models import Answer, Question, Survey

# Register your models here.
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass