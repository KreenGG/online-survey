from typing import Any
from django.forms import BaseModelForm
from django.shortcuts import redirect
from core.apps.surveys.forms import SurveyForm
from core.apps.surveys.models import Answer, Question, Survey
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView


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
    

class SurveyTakeFormView(CreateView):
    form_class = SurveyForm
    template_name = "surveys/survey_form.html"
    survey_id = None
    
    def get_form(self, form_class: type[SurveyForm] | None = ...) -> SurveyForm:
        self.survey_id = self.request.resolver_match.kwargs.pop("pk")
        survey = Survey.objects.get(pk=self.survey_id)
        return SurveyForm(survey)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(pk=self.survey_id)
        return context
