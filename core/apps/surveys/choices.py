from collections import namedtuple
from enum import Enum
from django import forms
from django.utils.translation import gettext_lazy as _
from django.db import models


# TYPE_FIELD = namedtuple(
#     'TYPE_FIELD', 'text rating'
# )._make(range(2))

# QUESTION_TYPE = [
#         (TYPE_FIELD.text, _("Text")),
#         (TYPE_FIELD.rating, _("Rating"))
#     ]

class QuestionType(models.IntegerChoices):
    TEXT = 0
    RATING = 1
