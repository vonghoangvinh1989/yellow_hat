from django.shortcuts import render

# from celery.result import AsyncResult


# Create your views here.
def index(request):
    return render(request, "main_app/index.html")
