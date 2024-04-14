import uuid
from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator

from core.apps.surveys.choices import QuestionType


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Survey(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", default='')

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.title


class Question(BaseModel):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, verbose_name="Опрос")
    title    = models.CharField(max_length=500, verbose_name="Вопрос", help_text="Введите свой вопрос")
    question_type = models.PositiveSmallIntegerField(choices=QuestionType, verbose_name="Тип вопроса")
    ordering = models.PositiveIntegerField(verbose_name="Упорядочивание", default=0,
        help_text=("Определяет порядок следования вопросов в опросе")
    )


    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["ordering"]

    def __str__(self):
        return f"{self.title} | Опрос-{self.survey.title}"


class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE, verbose_name=("Вопрос"))
    value = models.TextField(verbose_name="Ответ", help_text="Ответ пользователя")
    

    class Meta:
        verbose_name = ("Ответ")
        verbose_name_plural = ("Ответы")
        ordering = ["question__ordering"]

    def __str__(self):
        return f"{self.question}: {self.value}"
