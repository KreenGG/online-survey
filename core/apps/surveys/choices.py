from django.db import models


class QuestionType(models.IntegerChoices):
    TEXT = 0
    RATING = 1
