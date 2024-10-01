from passive_recon.models import Tool


def get_passive_recon_tools():
    """Retrieve all passive reconnaissance tools."""
    return Tool.objects.all()
