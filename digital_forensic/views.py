from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import DigitalForensicTool
from django.contrib.auth.decorators import login_required
from yellow_hat.constants import VOLATILITY


# Create your views here.
def index(request):
    return render(request, "digital_forensic/index.html")


@login_required
def digital_forensic_tools(request, forensic_tool_slug):
    digital_tool = DigitalForensicTool.objects.get(slug=forensic_tool_slug)
    digital_tool_name = digital_tool.name.strip().lower()
    target_domain = ""

    try:
        if request.method == "GET":
            if digital_tool_name in VOLATILITY:
                return render(
                    request,
                    "digital_forensic/volatility.html",
                    {
                        "digital_tool": digital_tool,
                    },
                )
        elif request.method == "POST":
            pass
    except DigitalForensicTool.DoesNotExist:
        raise Http404("Digital Forensic Tool does not exist")
