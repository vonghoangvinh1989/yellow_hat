from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os


# Create your views here.
def index(request):
    return render(request, "report/index.html")


@csrf_exempt
def save_report(request):
    print("Go to function save_report in backend")
    if request.method == "POST":
        file_type = request.POST.get("file_type", "").strip().lower()
        table_from = request.POST.get("table_from", "").strip().lower()

        print(f"file_type is {file_type}")
        print(f"table_from is {table_from}")

        if file_type == "pdf" and table_from == "tabulator":
            print("Go here mean select correct type")
            pdf = request.FILES["pdf"]

            print(f"pdf content is {pdf}")
            save_path = os.path.join(settings.MEDIA_ROOT, "report_directory", pdf.name)

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
                file_path = default_storage.save(
                    os.path.join("report_directory", pdf.name), pdf
                )
                return JsonResponse(
                    {"message": "Report saved successfully.", "file_path": file_path},
                    status=200,
                )
        return JsonResponse({"error": "No file uploaded."}, status=400)
