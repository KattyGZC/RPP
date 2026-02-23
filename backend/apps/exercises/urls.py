from django.urls import path

from .views import ExerciseDetailView, ExerciseListView, LevelListView, StudentProgressView, UserProgressView

urlpatterns = [
    path("levels/", LevelListView.as_view(), name="levels"),
    path("", ExerciseListView.as_view(), name="exercises"),
    path("<int:exercise_id>/", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("progress/", UserProgressView.as_view(), name="my-progress"),
    path("progress/<int:user_id>/", StudentProgressView.as_view(), name="student-progress"),
]
