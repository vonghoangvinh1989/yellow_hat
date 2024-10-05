from active_recon.models import ActiveReconTool


def get_active_recon_tools():
    return ActiveReconTool.objects.all()
