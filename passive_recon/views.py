from django.shortcuts import render
from django.http import Http404
from .models import Tool
from .utils import dnspython_utils
from passive_recon.utils.passive_recon_tools import get_passive_recon_tools

# constant variables
from yellow_hat.constants import NSLOOKUP


# Create your views here.
def index(request):
    return render(
        request,
        "passive_recon/index.html",
        {"passive_recon_tools": get_passive_recon_tools()},
    )


def passive_recon_tools(request, passive_tool_slug):
    try:
        passive_tool = Tool.objects.get(slug=passive_tool_slug)
        passive_tool_name = passive_tool.name.strip().lower()

        if request.method == "GET":
            if passive_tool_name in NSLOOKUP:
                return render(
                    request,
                    "passive_recon/nslookup.html",
                    {
                        "passive_tool": passive_tool,
                        "passive_recon_tools": get_passive_recon_tools(),
                    },
                )
        elif request.method == "POST":
            # clean post data
            target_domain = request.POST.get("domain").strip().lower()
            scanning_result = ""
            error_message = ""
            if len(target_domain):
                scanning_result = dnspython_utils.scan_domain(target_domain)
                return render(
                    request,
                    "passive_recon/nslookup.html",
                    {
                        "passive_tool": passive_tool,
                        "passive_recon_tools": get_passive_recon_tools(),
                        "scanning_result": scanning_result,
                        "error_message": error_message,
                    },
                )
            else:
                error_message = "Please enter a valid domain."
                return render(
                    request,
                    "passive_recon/nslookup.html",
                    {
                        "passive_tool": passive_tool,
                        "passive_recon_tools": get_passive_recon_tools(),
                        "scanning_result": scanning_result,
                        "error_message": error_message,
                    },
                )
    except Tool.DoesNotExist:
        raise Http404("Passive Recon Tool does not exist")
