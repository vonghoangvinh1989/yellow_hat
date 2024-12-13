from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import DigitalForensicTool
from django.contrib.auth.decorators import login_required
from yellow_hat.constants import VOLATILITY, REGIPY
from regipy.registry import RegistryHive
import pandas as pd
import csv
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
            elif digital_tool_name in REGIPY:
                return render(
                    request,
                    "digital_forensic/regipy.html",
                    {
                        "digital_tool": digital_tool,
                    },
                )
        elif request.method == "POST":
            if digital_tool_name in VOLATILITY:
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
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
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
            elif digital_tool_name in REGIPY:
                registry_dump = request.FILES.get("registry-dump")

                if not registry_dump:
                    return JsonResponse(
                        {"error": "No registry dump file uploaded."}, status=400
                    )

                # Define paths for temporary files
                dump_file_path = os.path.join(
                    settings.DUMP_FILES_DIRECTORY, "temp_registry_dump.raw"
                )
                csv_file_path = os.path.join(
                    settings.DUMP_FILES_DIRECTORY, "registry_dump.csv"
                )

                # Save the uploaded file temporarily
                with open(dump_file_path, "wb") as f:
                    for chunk in registry_dump.chunks():
                        f.write(chunk)

                try:
                    print("Registry dump")
                    # Run the regipy-dump command
                    subprocess.run(
                        ["regipy-dump", dump_file_path, "-o", csv_file_path], check=True
                    )

                    # Preprocess the CSV file to handle inconsistencies
                    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
                        reader = csv.reader(csvfile)
                        headers = next(reader)
                        rows = [row for row in reader if len(row) == len(headers)]

                    # Create a DataFrame from the preprocessed rows
                    df = pd.DataFrame(rows, columns=headers)

                    # Convert the DataFrame to a dictionary
                    csv_data = df.to_dict(orient="records")

                    # Cleanup temporary files
                    os.remove(dump_file_path)
                    os.remove(csv_file_path)

                    # Return the CSV data as JSON
                    return JsonResponse({"result": csv_data}, status=200)
                except subprocess.CalledProcessError as error:
                    os.remove(dump_file_path)
                    return JsonResponse({"error": str(error)}, status=500)
                except Exception as error:
                    if os.path.exists(dump_file_path):
                        os.remove(dump_file_path)
                    if os.path.exists(csv_file_path):
                        os.remove(csv_file_path)
                    return JsonResponse({"error": str(error)}, status=500)
    except DigitalForensicTool.DoesNotExist:
        raise Http404("Digital Forensic Tool does not exist")
