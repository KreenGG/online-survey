from django.urls import path

from core.apps.surveys import views

urlpatterns = [
    path("", views.index, name="index"),
    path('surveys/dashboard', views.SurveyListView.as_view(), name='dashboard'),
    path("surveys/<uuid:pk>/", views.show_survey, name="survey-take-form"),
]
