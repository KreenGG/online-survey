from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from core.apps.surveys.models import Answer, Question, Survey, SurveyTake


class QuestionInline(admin.TabularInline):
    model = Question
    sortable_by = ["ordering"]


class AnswerInline(admin.TabularInline):
    model = Answer
    readonly_fields = ["question", "value"]
    can_delete = False
    extra = 0
    max_num = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    inlines = [QuestionInline]
    list_display = ["title", "questions_count", "link", "created_at"]

    @admin.display(description="Cсылка на опрос")
    def link(self, survey):
        return format_html(f"<a href={survey.get_absolute_url()}>Перейти на опрос</a>")

    @admin.display(description="Количество вопросов")
    def questions_count(self, survey):
        return survey.questions.count()


@admin.register(SurveyTake)
class SurveyTakeAdmin(admin.ModelAdmin):
    list_display = ["id", "survey_link", "taked_at"]
    list_filter = ["survey"]
    inlines = [AnswerInline]
    search_fields = ["survey__title"]
    ordering = ["survey"]

    @admin.display(description="Дата прохождения")
    def taked_at(self, survey):
        return survey.created_at

    @admin.display(description="Опрос")
    def survey_link(self, question):
        url = (
            reverse("admin:surveys_survey_changelist")
            + str(question.survey_id)
            + "/change"
        )
        return format_html(f"<a href={url}>{question.survey.title}</a>")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "survey_link"]
    list_filter = ["survey"]
    search_fields = ["title"]
    ordering = ["survey"]

    def get_model_perms(self, request):
        """Return empty perms dict thus hiding the model from admin index."""
        return {}

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
    list_display = [
        "survey_link",
        "question",
        "value",
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
