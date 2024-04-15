from django.urls import path, include

from core.apps.surveys import views


urlpatterns = [
    path("", views.index, name="index"),
    path('surveys/dashboard', views.SurveyListView.as_view(), name='dashboard'),
    path("surveys/<uuid:pk>/", views.SurveyTakeFormView.as_view(), name="survey-form"),
]