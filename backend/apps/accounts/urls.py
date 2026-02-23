from django.urls import path

from .views import MeView, RegisterView, StudentListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("students/", StudentListView.as_view(), name="students"),
]
