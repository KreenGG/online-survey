from typing import Any
from django.forms import BaseModelForm
from core.apps.surveys.forms import SurveyForm
from core.apps.surveys.models import Question, Survey
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView





class SurveyListView(ListView):
    model = Survey
    title_page = 'Survey List'
    # template_name = 'survey_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["surveys"] = Survey.objects.all()
        return context


# class SurveyDetailView(DetailView):
#     model = Survey
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         survey = context["object"]
#         context["questions"] = survey.questions.all()
        
#         return context


class SurveyFormView(CreateView):
    form_class = SurveyForm
    template_name = "surveys/survey_form.html"
    
    def get_form(self, form_class: type[SurveyForm] | None = ...) -> SurveyForm:
        survey = Survey.objects.get(pk=self.request.path.strip("/"))
        return SurveyForm(survey)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(pk=self.request.path.strip("/"))
        return context
