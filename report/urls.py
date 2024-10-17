from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="report"),
    path("save-report/", views.save_report, name="save-report"),
    path("merge-report/", views.merge_report, name="merge-report"),
    path("delete-report/", views.delete_report, name="delete-report"),
]
