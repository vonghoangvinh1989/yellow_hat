from django.shortcuts import render
from django.http import Http404
from .models import Tool
from .utils import dnspython_utils, whois_utils
from passive_recon.utils.passive_recon_tools import get_passive_recon_tools

# constant variables
from yellow_hat.constants import NSLOOKUP, WHOIS


# Create your views here.
def index(request):
    return render(
        request,
        "passive_recon/index.html",
        {"passive_recon_tools": get_passive_recon_tools()},
    )


def passive_recon_tools(request, passive_tool_slug):
    passive_tool = Tool.objects.get(slug=passive_tool_slug)
    passive_tool_name = passive_tool.name.strip().lower()

    try:
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
            elif passive_tool_name in WHOIS:
                return render(
                    request,
                    "passive_recon/whois.html",
                    {
                        "passive_tool": passive_tool,
                        "passive_recon_tools": get_passive_recon_tools(),
                    },
                )
        elif request.method == "POST":
            # clean post data
            target_domain = request.POST.get("domain").strip().lower()
            scanning_result = None
            error_message = None
            if len(target_domain):
                if passive_tool_name in NSLOOKUP:
                    try:
                        scanning_nslookup_result = dnspython_utils.scan_domain(
                            target_domain
                        )
                    except Exception as error:
                        error_message = error

                    return render(
                        request,
                        "passive_recon/nslookup.html",
                        {
                            "passive_tool": passive_tool,
                            "passive_recon_tools": get_passive_recon_tools(),
                            "scanning_result": scanning_nslookup_result,
                            "error_message": error_message,
                        },
                    )
                elif passive_tool_name in WHOIS:
                    print(f"passive_tool_name is {passive_tool_name}")
                    print(f"target domain is: {target_domain}")
                    try:
                        scanning_whois_result = whois_utils.scan_whois(target_domain)
                    except Exception as error:
                        error_message = error

                    return render(
                        request,
                        "passive_recon/whois.html",
                        {
                            "passive_tool": passive_tool,
                            "passive_recon_tools": get_passive_recon_tools(),
                            "scanning_result": scanning_whois_result,
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
