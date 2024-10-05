from django.shortcuts import render
from django.http import Http404
from .models import ActiveReconTool

# constant variables
from yellow_hat.constants import NMAP


# Create your views here.
def index(request):
    return render(request, "active_recon/index.html")


def active_recon_tools(request, active_tool_slug):
    active_tool = ActiveReconTool.objects.get(slug=active_tool_slug)
    active_tool_name = active_tool.name.strip().lower()
    target_domain = ""

    try:
        if request.method == "GET":
            if active_tool_name in NMAP:
                return render(
                    request,
                    "active_recon/nmap.html",
                    {
                        "active_tool": active_tool,
                    },
                )
        elif request.method == "POST":
            pass
    except ActiveReconTool.DoesNotExist:
        raise Http404("Active Recon Tool does not exist")
