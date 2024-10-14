from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="report"),
    path("save-report/", views.save_report, name="save-report"),
]
