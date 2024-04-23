from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView

from core.apps.surveys.forms import SurveyTakeForm
from core.apps.surveys.models import Answer, Question, Survey
from core.apps.surveys.services import SurveyService


def index(request):
    return render(request, "surveys/index.html")


class SurveyListView(ListView):
    model = Survey
    title_page = 'Survey List'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def show_survey(request, pk):
    service = SurveyService()
    survey = get_object_or_404(Survey, pk=pk)
    form = SurveyTakeForm(survey)

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
        request.session[str(survey.id)] = False
        return redirect("/")

    context = {
      "survey": survey,
      "form": form,
      "can_take_survey": service.can_take_survey(request, survey),
      "survey_edit_link": service.get_edit_link(survey),
      "participants": service.get_participants_number(survey),
      "rating_questions": service.get_rating_questions(survey),
      "text_questions": service.get_text_questions(survey),     # TODO: сделать обзор ответов по вопросам
    }

    return render(request, "surveys/survey_take_form.html", context)
