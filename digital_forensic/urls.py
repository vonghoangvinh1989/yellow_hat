from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="digital-forensic"),
    path(
        "<slug:forensic_tool_slug>",
        views.digital_forensic_tools,
        name="digital-forensic-tools",
    ),
]
