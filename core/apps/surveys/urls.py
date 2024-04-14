from django.urls import path, include

from core.apps.surveys import views


urlpatterns = [
    path('', views.SurveyListView.as_view(), name='index'),
    path("<uuid:pk>/", views.SurveyFormView.as_view(), name="survey-form"),
]