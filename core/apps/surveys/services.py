from django.urls import reverse

from core.apps.surveys.choices import QuestionType
from core.apps.surveys.models import Answer, Question, Survey


class SurveyService:
    def get_participants_number(self, survey: Survey) -> int:
        first_question = Question.objects.filter(survey=survey).first()
        participants = Answer.objects.filter(question=first_question).count()
        return participants

    def get_edit_link(self, survey: Survey) -> str:
        survey_edit_link = (
            reverse("admin:surveys_survey_changelist")
            + str(survey.id)
            + "/change"
        )
        return survey_edit_link

    def get_rating_questions(self, survey: Survey):
        rating_questions = Question.objects.filter(
            survey=survey, question_type=QuestionType.RATING,
        )

        question_avg = []
        for question in rating_questions:
            answers = Answer.objects.filter(question=question)
            rating = 0
            if len(answers) == 0:
                avg_rating = 0
            else:
                for answer in answers:
                    rating += int(answer.value)
                    avg_rating = round(rating / len(answers), 2)
            question_avg.append({"question": question, "avg_rating": avg_rating})
        return question_avg

    def get_text_questions(self, survey: Survey) -> list[Question]:
        text_questions = Question.objects.filter(
            survey=survey, question_type=QuestionType.TEXT,
        )
        return text_questions

    def get_choices_questions(self, survey: Survey) -> list[Question]:
        hoices_questions = Question.objects.filter(
            survey=survey, question_type=QuestionType.CHOICES,
        )
        return hoices_questions

    def can_take_survey(self, request, survey: Survey) -> bool:
        return request.session.get(str(survey.id), True)
