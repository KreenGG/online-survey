from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.list import ListView

from core.apps.surveys.forms import SurveyTakeForm
from core.apps.surveys.models import Answer, Question, Survey


def index(request):
    return render(request, "surveys/index.html")


class SurveyListView(ListView):
    model = Survey
    title_page = 'Survey List'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def show_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    form = SurveyTakeForm(survey)

    survey_edit_link = (
        reverse("admin:surveys_survey_changelist")
        + str(survey.id)
        + "/change"
    )

    context = {
      "survey": survey,
      "form": form,
      "survey_edit_link": survey_edit_link,
    }

    if request.method == "POST":
        form = SurveyTakeForm(survey, request.POST)

        for question in form.data:
            if question.startswith("question_"):
                question_id = question.removeprefix("question_")
                value = form.data.get(question)

                Answer.objects.create(
                    question=Question.objects.get(pk=question_id),
                    value=value,
                )
        # TODO: Сделать страницу успешного прохождения и редиректить туда
        return redirect("/")

    return render(request, "surveys/survey_take_form.html", context)
