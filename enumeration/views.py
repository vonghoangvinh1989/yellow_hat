from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import EnumerationTool
from .utils import pysnmp_utils, subdomain_utils, email_finder_utils
from django.conf import settings
import asyncio


# constant variables
from yellow_hat.constants import SNMP_WALK, SUBDOMAIN, EMAIL_FINDER


# Create your views here.
def index(request):
    return render(request, "enumeration/index.html")


def enumeration_tools(request, enumeration_tool_slug):
    enumeration_tool = EnumerationTool.objects.get(slug=enumeration_tool_slug)
    enumeration_tool_name = enumeration_tool.name.strip().lower()
    print(f"Enumeration tool name is: {enumeration_tool_name}")

    try:
        if request.method == "GET":
            if enumeration_tool_name in SNMP_WALK:
                return render(
                    request,
                    "enumeration/snmpwalk.html",
                    {
                        "enumeration_tool": enumeration_tool,
                    },
                )
            elif enumeration_tool_name in SUBDOMAIN:
                return render(
                    request,
                    "enumeration/subdomain.html",
                    {
                        "enumeration_tool": enumeration_tool,
                    },
                )
            elif enumeration_tool_name in EMAIL_FINDER:
                return render(
                    request,
                    "enumeration/email-finder.html",
                    {
                        "enumeration_tool": enumeration_tool,
                    },
                )
        elif request.method == "POST":
            target_domain = request.POST.get("domain").strip().lower()

            # set default values for error and response data
            error_message = None
            response_data = None

            # set scanning result
            scanning_snmp_result = None

            if not target_domain:
                error_message = str("Please enter a valid domain name.")
                response_data = {
                    "error_message": error_message,
                }
                return JsonResponse(response_data)

            if enumeration_tool_name in SNMP_WALK:
                try:
                    scanning_snmp_result = asyncio.run(
                        pysnmp_utils.snmp_walk(target_domain, "public")
                    )

                    if not scanning_snmp_result:
                        response_data = {
                            "scanning_result": "No result found.",
                        }

                        return JsonResponse(response_data, safe=False)
                except Exception as err:
                    error_message = str(err)

                response_data = {
                    "scanning_result": scanning_snmp_result,
                    "error_message": error_message,
                }
            elif enumeration_tool_name in SUBDOMAIN:
                try:
                    scanning_subdomain_result = (
                        subdomain_utils.enumerate_subdomains_securitytrails(
                            target_domain, settings.SECURITY_TRAILS
                        )
                    )

                    if not scanning_subdomain_result:
                        response_data = {
                            "scanning_result": "No result found.",
                        }

                        return JsonResponse(response_data, safe=False)
                except Exception as err:
                    error_message = str(err)

                response_data = {
                    "scanning_result": scanning_subdomain_result,
                    "error_message": error_message,
                }
            elif enumeration_tool_name in EMAIL_FINDER:
                try:
                    scanning_email_result = email_finder_utils.get_all_info_from_domain(
                        target_domain, settings.HUNTER_IO
                    )

                    if not scanning_email_result:
                        response_data = {
                            "scanning_result": "No result found.",
                        }

                        return JsonResponse(response_data, safe=False)
                except Exception as err:
                    error_message = str(err)

                response_data = {
                    "scanning_result": scanning_email_result,
                    "error_message": error_message,
                }
            else:
                error_message = str("Not using Enumeration Tool")
                response_data = {
                    "error_message": error_message,
                }

            return JsonResponse(response_data, safe=False)
    except EnumerationTool.DoesNotExist:
        raise Http404("Enumeration Tool does not exist")
