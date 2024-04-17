from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models import F

from core.apps.surveys.models import Answer, Question, Survey


class QuestionInline(admin.TabularInline):
    model = Question
    sortable_by = ["ordering"]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    inlines = [QuestionInline]
    list_display = ["title", "questions_count", "link"]
    
    
    @admin.display(description="Cсылка на опрос")
    def link(self, survey):
        return format_html(f"<a href={survey.get_absolute_url()}>Перейти на опрос</a>")
    
    @admin.display(description="Количество вопросов")
    def questions_count(self, survey):
        return survey.questions.count()



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "survey_link"]
    list_filter = ["survey"]
    search_fields = ["title"]
    ordering = ["survey"]

    @admin.display(description="Опрос")
    def survey_link(self, question):
        url = (
            reverse("admin:surveys_survey_changelist")
            + str(question.survey_id)
            + "/change"
        )
        return format_html(f"<a href={url}>{question.survey.title}</a>")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display =[
        "question",
        "value",
        "survey_link",
    ]
    readonly_fields = [field.name for field in Answer._meta.get_fields()]
    list_filter = ["question__survey_id"]
    
    def get_queryset(self, request):
        return Answer.objects.select_related("question")
    
    @admin.display(description="Опрос")
    def survey_link(self, answer):
        url = (
            reverse("admin:surveys_survey_changelist")
            + str(answer.question.survey_id)
            + "/change"
        )
        return format_html(f"<a href={url}>{answer.question.survey.title}</a>")