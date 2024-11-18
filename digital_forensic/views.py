from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import DigitalForensicTool
from django.contrib.auth.decorators import login_required
from yellow_hat.constants import VOLATILITY
import os
import subprocess
from django.conf import settings


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
            memory_dump = request.FILES.get("memory-dump")
            volatility_plugin = request.POST.get("plugin")

            if not memory_dump:
                return JsonResponse(
                    {"error": "No memory dump file uploaded."}, status=400
                )

            if not volatility_plugin:
                return JsonResponse({"error": "No plugin selected."}, status=400)

            dump_file_path = os.path.join(
                settings.DUMP_FILES_DIRECTORY, "temp_memory_dump.raw"
            )

            with open(dump_file_path, "wb") as f:
                for chunk in memory_dump.chunks():
                    f.write(chunk)

            print(f"volatility_plugin is {volatility_plugin}")

            if volatility_plugin == "windows.registry.printkey":
                command = [
                    "python",
                    settings.VOLATILITY_PATH,
                    "-f",
                    dump_file_path,
                    "--plugin-dirs",
                    settings.VOLATILITY_PLUGINS_PATH,
                    "--symbol-dir",
                    settings.VOLATILITY_SYMBOLS_PATH,
                    volatility_plugin,
                    "--key",
                    "Software\\Microsoft\\Windows\\CurrentVersion",
                    "--recurse",
                ]
            else:
                command = [
                    "python",
                    settings.VOLATILITY_PATH,
                    "-f",
                    dump_file_path,
                    "--plugin-dirs",
                    settings.VOLATILITY_PLUGINS_PATH,
                    "--symbol-dir",
                    settings.VOLATILITY_SYMBOLS_PATH,
                    volatility_plugin,
                ]

            try:
                result = subprocess.run(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                output = result.stdout
                error = result.stderr
            except Exception as e:
                print(f"error is: {e}")
                output = ""
                error = str(e)

            print(f"output is: {output}")

            # remove dump file
            os.remove(dump_file_path)
            return JsonResponse({"result": output, "error": error})
    except DigitalForensicTool.DoesNotExist:
        raise Http404("Digital Forensic Tool does not exist")
