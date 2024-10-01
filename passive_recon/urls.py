from django.urls import path
from . import views

urlpatterns = [
    path(
        "<slug:passive_tool_slug>",
        views.passive_recon_tools,
        name="passive-recon-tools",
    ),
]
