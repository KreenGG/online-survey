from django.db import models


class QuestionType(models.IntegerChoices):
    TEXT = 0, "Текст"
    RATING = 1, "Рейтинг"
    CHOICES = 2, "С выбором"
