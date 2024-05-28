import os

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView

from core.apps.surveys.forms import SurveyTakeForm
from core.apps.surveys.models import Answer, Question, Survey, SurveyTake
from core.apps.surveys.reports import create_report
from core.apps.surveys.services import SurveyService
from core.project import settings


def index(request):
    return render(request, "surveys/index.html")


class SurveyListView(ListView):
    model = Survey
    title_page = 'Survey List'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def show_succes_page(request):
    return render(request, "surveys/success_page.html")


def get_report(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    create_report(survey)

    file_path = os.path.join(settings.MEDIA_ROOT, f"{survey.pk}.xlsx")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def show_survey(request, pk):
    service = SurveyService()
    survey = get_object_or_404(Survey, pk=pk)
    form = SurveyTakeForm(survey)

    if request.method == "POST":
        form = SurveyTakeForm(survey, request.POST)

        survey_take = SurveyTake.objects.create(survey=survey)
        for question in form.data:
            if question.startswith("question_"):
                question_id = question.removeprefix("question_")
                value = form.data.get(question)

                Answer.objects.create(
                    question=Question.objects.get(pk=question_id),
                    value=value,
                    survey_take=survey_take,
                )
        request.session[str(survey.id)] = False
        return redirect("success-page")

    context = {
      "survey": survey,
      "form": form,
      "can_take_survey": service.can_take_survey(request, survey),
      "survey_edit_link": service.get_edit_link(survey),
      "participants": service.get_participants_number(survey),
      "rating_questions": service.get_rating_questions(survey),
    }

    return render(request, "surveys/survey_take_form.html", context)
