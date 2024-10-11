from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import EnumerationTool

# constant variables
from yellow_hat.constants import (
    SNMP_WALK,
)


# Create your views here.
def index(request):
    return render(request, "enumeration/index.html")


def enumeration_tools(request, enumeration_tool_slug):
    enumeration_tool = EnumerationTool.objects.get(slug=enumeration_tool_slug)
    enumeration_tool_name = enumeration_tool.name.strip().lower()

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
        elif request.method == "POST":
            target_domain = request.POST.get("domain").strip().lower()

            # set default values for error and response data
            error_message = None
            response_data = None

            # TODO TODO TODO

    except EnumerationTool.DoesNotExist:
        raise Http404("Enumeration Tool does not exist")
