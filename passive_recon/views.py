from django.shortcuts import render
from django.http import Http404
from .models import Tool
from .utils import dnspython_utils

# constant variables
NSLOOKUP = ["nslookup"]


# Create your views here.
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
                    },
                )
        elif request.method == "POST":
            # clean post data
            target_domain = request.POST.get("domain").strip().lower()
            if len(target_domain):
                scanning_result = dnspython_utils.scan_domain(target_domain)
                return render(
                    request,
                    "passive_recon/nslookup.html",
                    {
                        "passive_tool": passive_tool,
                        "scanning_result": scanning_result,
                    },
                )
    except Tool.DoesNotExist:
        raise Http404("Passive Recon Tool does not exist")
