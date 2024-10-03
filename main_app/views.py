from django.shortcuts import render
from passive_recon.utils.passive_recon_tools import get_passive_recon_tools
from django.http import JsonResponse

# from celery.result import AsyncResult


# Create your views here.
def index(request):
    return render(
        request,
        "main_app/index.html",
        {"passive_recon_tools": get_passive_recon_tools()},
    )
