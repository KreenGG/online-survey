from django import forms

from core.apps.surveys.choices import QuestionType


class SurveyTakeForm(forms.Form):
    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        for question in survey.questions.all():
            match question.question_type:
                case QuestionType.TEXT :
                    self.fields[f"question_{question.id}"] = forms.CharField(
                        widget=forms.TextInput(
                            attrs={"class": "form-control"})
                    )
                    
                case QuestionType.RATING:                    
                    self.fields[f"question_{question.id}"] = forms.ChoiceField(
                        choices=[(1, 1 ), (2, 2 ), (3, 3), (4, 4), (5, 5)],
                        widget=forms.Select(
                            attrs={"class": "form-select"}), 
                    )
            
            self.fields[f"question_{question.id}"].label = question.title
            # self.fields[f"question_{question.id}"].widget.attrs.update({"class": "form-control"})
