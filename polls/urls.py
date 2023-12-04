from django.urls import path

from .views import SubmitAnswerView

urlpatterns = [path("submit_answer/", SubmitAnswerView.as_view(), name="submit-answer")]
