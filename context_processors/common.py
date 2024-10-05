from passive_recon.utils.passive_recon_tools import get_passive_recon_tools
from active_recon.utils.active_recon_tools import get_active_recon_tools


def common_context(request):
    return {
        "passive_recon_tools": get_passive_recon_tools(),
        "active_recon_tools": get_active_recon_tools(),
    }
