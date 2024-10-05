from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="active-recon"),
    path(
        "<slug:active_tool_slug>",
        views.active_recon_tools,
        name="active-recon-tools",
    ),
]
