from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="enumeration"),
    path(
        "<slug:enumeration_tool_slug>",
        views.enumeration_tools,
        name="enumeration-tools",
    ),
]
