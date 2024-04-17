from django.shortcuts import get_object_or_404, redirect, render
from core.apps.surveys.forms import SurveyTakeForm
from core.apps.surveys.models import Answer, Question, Survey
from django.views.generic.list import ListView


def index(request):
    # Сделать auth
    return redirect("dashboard")


class SurveyListView(ListView):
    model = Survey
    title_page = 'Survey List'
    # template_name = 'survey_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["surveys"] = Survey.objects.all()
        return context
    
def show_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    form = SurveyTakeForm(survey)
    
    context = {
      "survey": survey,
      "form": form,
    }
    
    if request.method == "POST":
        form = SurveyTakeForm(survey, request.POST)
        
        for question in form.data:
            if question.startswith("question_"):
                question_id = question.removeprefix("question_")
                value = form.data.get(question)

                Answer.objects.create(
                    question = Question.objects.get(pk=question_id),
                    value = value
                )
        # TODO: Сделать страницу успешного прохождения и редиректить туда
        return redirect("/")

    return render(request, "surveys/survey_take_form.html", context)