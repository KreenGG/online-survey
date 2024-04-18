from django.urls import path

from core.apps.surveys import views

urlpatterns = [
    path("", views.index, name="index"),
    path("surveys/<uuid:pk>/", views.show_survey, name="survey-take-form"),
]
