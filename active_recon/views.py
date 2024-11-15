from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import ActiveReconTool
from .utils import python3_nmap_utils
from django.contrib.auth.decorators import login_required

# constant variables
from yellow_hat.constants import (
    NMAP,
    NMAP_SCAN_TYPES,
    VERSION_DETECTION_SCAN,
    TOP_PORTS_SCAN,
)


# Create your views here.
def index(request):
    return render(request, "active_recon/index.html")


@login_required
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
                        "nmap_scan_types": NMAP_SCAN_TYPES,
                    },
                )
        elif request.method == "POST":
            target_domain = request.POST.get("domain").strip().lower()
            scan_type = request.POST.get("scan-type").strip().lower()

            print(f"Target domain is {target_domain}")
            print(f"Scan Type is {scan_type}")

            # set default values for error and response data
            error_message = None
            response_data = None

            # title for scanning result
            scanning_nmap_result = None

            if not target_domain:
                error_message = str("Please enter a valid domain name.")
                response_data = {
                    "error_message": error_message,
                }
                return JsonResponse(response_data)

            if not scan_type:
                error_message = str("Scan type is required for scanning.")
                response_data = {
                    "error_message": error_message,
                }
                return JsonResponse(response_data)

            if active_tool_name in NMAP:
                if not python3_nmap_utils.is_valid_scan_type(scan_type):
                    error_message = str("Scan type is not valid.")
                    response_data = {
                        "error_message": error_message,
                    }
                    return JsonResponse(response_data)
                else:
                    print("Go here mean correct scan type")
                    if scan_type == TOP_PORTS_SCAN:
                        try:
                            print("go here to calling nmap top port scan")
                            scanning_nmap_result = (
                                python3_nmap_utils.nmap_top_ports_scan(target_domain)
                            )
                        except Exception as err:
                            print(f"error is: {err}")
                            error_message = str(err)

                        response_data = {
                            "scan_type": TOP_PORTS_SCAN,
                            "scanning_result": scanning_nmap_result,
                            "error_message": error_message,
                        }
                    elif scan_type == VERSION_DETECTION_SCAN:
                        try:
                            print(f"go here to calling nmap version detection scan")
                            scanning_nmap_result = (
                                python3_nmap_utils.nmap_version_detection(target_domain)
                            )
                        except Exception as err:
                            print(f"error is: {err}")
                            error_message = str(err)

                        response_data = {
                            "scan_type": VERSION_DETECTION_SCAN,
                            "scanning_result": scanning_nmap_result,
                            "error_message": error_message,
                        }

                    # return response
                    return JsonResponse(response_data)
            else:
                error_message = str("Not using NMAP Tool")
                response_data = {
                    "error_message": error_message,
                }
                return JsonResponse(response_data)
    except ActiveReconTool.DoesNotExist:
        raise Http404("Active Recon Tool does not exist")
