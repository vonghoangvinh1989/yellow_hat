from django.shortcuts import render
from passive_recon.models import Tool


# Create your views here.
def index(request):
    passive_recon_tools = Tool.objects.all()
    return render(
        request, "main_app/index.html", {"passive_recon_tools": passive_recon_tools}
    )
