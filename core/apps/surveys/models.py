import uuid

from django.db import models

from core.apps.surveys.choices import QuestionType


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class Survey(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)     # noqa
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", default='')

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/surveys/{self.id}/"


class SurveyTake(BaseModel):
    survey = models.ForeignKey(Survey, related_name='takes', on_delete=models.CASCADE, verbose_name="Опрос")

    def __str__(self) -> str:
        return f"{self.survey.title} | прохождение #{self.id}"

    class Meta:
        verbose_name = "Прохождение опроса"
        verbose_name_plural = "Прохождения опросов"
        ordering = ["-created_at"]


class Question(BaseModel):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, verbose_name="Опрос")
    title = models.CharField(max_length=500, verbose_name="Вопрос", help_text="Введите свой вопрос")
    question_type = models.PositiveSmallIntegerField(choices=QuestionType, verbose_name="Тип вопроса")
    ordering = models.PositiveIntegerField(
        verbose_name="Упорядочивание", default=0,
        help_text=("Определяет порядок следования вопросов в опросе"),
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["ordering"]

    def __str__(self):
        return f"{self.title}"


class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE, verbose_name=("Вопрос"))
    value = models.TextField(verbose_name="Ответ", help_text="Ответ пользователя")
    survey_take = models.ForeignKey(SurveyTake, on_delete=models.CASCADE, verbose_name="Номер прохождения опроса")

    class Meta:
        verbose_name = ("Ответ")
        verbose_name_plural = ("Ответы")
        ordering = ["question__ordering"]

    def __str__(self):
        return f"{self.question}: {self.value}"
