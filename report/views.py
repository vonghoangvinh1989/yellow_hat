from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from PyPDF2 import PdfMerger
from datetime import datetime
from yellow_hat.constants import NORMAL_CATEGORIES, MERGE_CATEGORIES
from django.contrib.auth.decorators import login_required
import os


# Create your views here.
@login_required
def index(request):
    if request.method == "GET":
        print("Go to function index of reporting")
        # Path to the report directory
        report_directory = os.path.join(settings.MEDIA_ROOT)

        # Initialize categories
        categories = {
            "Planning and Scoping Reports": [],
            "Passive Reconnaissance Reports": [],
            "Active Reconnaissance Reports": [],
            "Vulnerability Assessment Reports": [],
            "Enumeration Reports": [],
            "Digital Forensic Reports": [],
            "Merge Reports": [],
            "Other Reports": [],
        }

        if os.path.exists(report_directory):
            report_files = os.listdir(report_directory)
            for file_name in report_files:
                if os.path.isfile(os.path.join(report_directory, file_name)):
                    if file_name.startswith("planning_scoping_"):
                        categories["Planning and Scoping Reports"].append(file_name)
                    elif file_name.startswith("passive_recon_"):
                        categories["Passive Reconnaissance Reports"].append(file_name)
                    elif file_name.startswith("active_recon_"):
                        categories["Active Reconnaissance Reports"].append(file_name)
                    elif file_name.startswith("vulnerability_assess_"):
                        categories["Vulnerability Assessment Reports"].append(file_name)
                    elif file_name.startswith("enumeration_"):
                        categories["Enumeration Reports"].append(file_name)
                    elif file_name.startswith("digital_forensic_"):
                        categories["Digital Forensic Reports"].append(file_name)
                    elif file_name.startswith("merge_"):
                        categories["Merge Reports"].append(file_name)
                    else:
                        categories["Other Reports"].append(file_name)

        # Pass the list of files to the template
        context = {
            "categories": categories,
            "media_url": settings.MEDIA_URL,
            "normal_categories": NORMAL_CATEGORIES,
            "merge_categories": MERGE_CATEGORIES,
        }

    return render(request, "report/index.html", context)


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


def delete_report(request):
    print("Go to function delete_report")
    if request.method == "POST":
        selected_reports = request.POST.get("reports", "").split(",")
        if not selected_reports:
            return JsonResponse({"error": "No reports selected."}, status=400)

        report_directory = os.path.join(settings.MEDIA_ROOT)

        for report in selected_reports:
            report_path = os.path.join(report_directory, report)
            if os.path.exists(report_path):
                os.remove(report_path)
            else:
                return JsonResponse(
                    {"error": f"Report {report} not found."}, status=404
                )

        return JsonResponse({"message": "Reports deleted successfully."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def merge_report(request):
    print("Go to function merge_report")
    if request.method == "POST":
        selected_reports = request.POST.get("reports", "").split(",")
        if not selected_reports:
            return JsonResponse({"error": "No reports selected."}, status=400)

        report_directory = os.path.join(settings.MEDIA_ROOT)
        merger = PdfMerger()

        for report in selected_reports:
            report_path = os.path.join(report_directory, report)
            if os.path.exists(report_path):
                merger.append(report_path)
            else:
                return JsonResponse(
                    {"error": f"Report {report} not found."}, status=404
                )

        # Create a filename with the current date and time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        merged_report_filename = f"merge_report_{timestamp}.pdf"
        merged_report_path = os.path.join(report_directory, merged_report_filename)

        with open(merged_report_path, "wb") as merged_report_file:
            merger.write(merged_report_file)
        merger.close()

        return JsonResponse(
            {
                "message": "Merge Report Successfully.",
                "file_path": merged_report_filename,
            },
            status=200,
        )
    return JsonResponse({"error": "Invalid request method."}, status=405)
