from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os


# Create your views here.
def index(request):
    if request.method == "GET":
        print("Go to function index of reporting")
        # Path to the report directory
        report_directory = os.path.join(settings.MEDIA_ROOT)

        # Initialize categories
        categories = {
            "Passive Reconnaissance Reports": [],
            "Active Reconnaissance Reports": [],
            "Vulnerability Assessment Reports": [],
            "Enumeration Reports": [],
        }

        if os.path.exists(report_directory):
            report_files = os.listdir(report_directory)
            for file_name in report_files:
                if os.path.isfile(os.path.join(report_directory, file_name)):
                    if file_name.startswith("passive_recon_"):
                        categories["Passive Reconnaissance Reports"].append(file_name)
                    elif file_name.startswith("active_recon_"):
                        categories["Active Reconnaissance Reports"].append(file_name)
                    elif file_name.startswith("vulnerability_assess_"):
                        categories["Vulnerability Assessment Reports"].append(file_name)
                    elif file_name.startswith("enumeration_"):
                        categories["Enumeration Reports"].append(file_name)
                    else:
                        categories["Other Reports"].append(file_name)

        # Pass the list of files to the template
        context = {
            "categories": categories,
            "media_url": settings.MEDIA_URL,
        }

    return render(request, "report/index.html", context)


@csrf_exempt
def save_report(request):
    if request.method == "POST":
        file_type = request.POST.get("file_type", "").strip().lower()
        table_from = request.POST.get("table_from", "").strip().lower()

        print(f"file_type is {file_type}")
        print(f"table_from is {table_from}")

        if file_type == "pdf" and table_from == "tabulator":
            print("Go here mean select correct type")
            pdf = request.FILES["pdf"]

            print(f"pdf content is {pdf}")
            save_path = os.path.join(settings.MEDIA_ROOT, pdf.name)

            with open(save_path, "wb") as f:
                for chunk in pdf.chunks():
                    f.write(chunk)

            return JsonResponse(
                {"message": "Report saved successfully.", "file_path": save_path},
                status=200,
            )
        else:
            pdf = request.FILES.get("pdf")
            if pdf:
                file_path = default_storage.save(os.path.join(pdf.name), pdf)
                return JsonResponse(
                    {"message": "Report saved successfully.", "file_path": file_path},
                    status=200,
                )
        return JsonResponse({"error": "No file uploaded."}, status=400)
