from django.urls import path

from core.apps.surveys import views

urlpatterns = [
    path("", views.index, name="index"),
    path("success", views.show_succes_page, name="success-page"),
    path("surveys/<uuid:pk>/", views.show_survey, name="survey-take-form"),
]
