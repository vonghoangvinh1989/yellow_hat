from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import Tool
from .utils import dnspython_utils, whois_utils
from django.contrib.auth.decorators import login_required
from yellow_hat.constants import NSLOOKUP, WHOIS


# Create your views here.
def index(request):
    return render(request, "passive_recon/index.html")


@login_required
def passive_recon_tools(request, passive_tool_slug):
    passive_tool = Tool.objects.get(slug=passive_tool_slug)
    passive_tool_name = passive_tool.name.strip().lower()
    target_domain = ""

    try:
        if request.method == "GET":
            if passive_tool_name in NSLOOKUP:
                return render(
                    request,
                    "passive_recon/nslookup.html",
                    {
                        "passive_tool": passive_tool,
                    },
                )
            elif passive_tool_name in WHOIS:
                return render(
                    request,
                    "passive_recon/whois.html",
                    {
                        "passive_tool": passive_tool,
                    },
                )
        elif request.method == "POST":
            # clean variables from post form
            target_domain = request.POST.get("domain").strip().lower()

            # set default values for error and response data
            error_message = None
            response_data = None

            # title for scanning result
            title = ""

            if len(target_domain):
                if passive_tool_name in NSLOOKUP:
                    # set title
                    title = "NSLOOKUP SCANNING RESULT\n"

                    try:
                        scanning_nslookup_result = dnspython_utils.scan_domain(
                            target_domain
                        )
                    except Exception as err:
                        error_message = str(err)

                    response_data = {
                        "scanning_result": f"{title} {scanning_nslookup_result}",
                        "error_message": error_message,
                    }
                elif passive_tool_name in WHOIS:
                    # set title
                    title = "WHOIS SCANNING RESULT\n"

                    try:
                        scanning_whois_result = whois_utils.scan_whois(target_domain)
                    except Exception as err:
                        error_message = str(err)

                    response_data = {
                        "scanning_result": f"{title} {scanning_whois_result}",
                        "error_message": error_message,
                    }
            else:
                error_message = str("Please enter a valid domain.")
                response_data = {
                    "error_message": error_message,
                }

            return JsonResponse(response_data)
    except Tool.DoesNotExist:
        raise Http404("Passive Recon Tool does not exist")
