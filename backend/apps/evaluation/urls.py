from django.urls import path

from .views import EvaluateReadingView

urlpatterns = [
    path("evaluate/", EvaluateReadingView.as_view(), name="evaluate"),
]
