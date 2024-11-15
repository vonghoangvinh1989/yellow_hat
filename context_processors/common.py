from passive_recon.utils.passive_recon_tools import get_passive_recon_tools
from active_recon.utils.active_recon_tools import get_active_recon_tools
from vulnerability_assessment.utils.vulnerability_assessment_tools import (
    get_vulnerability_assessment_tools,
)
from enumeration.utils.enumeration_tools import get_enumeration_tools
from digital_forensic.utils.digital_forensic_tools import get_digital_forensic_tools


def common_context(request):
    return {
        "passive_recon_tools": get_passive_recon_tools(),
        "active_recon_tools": get_active_recon_tools(),
        "vulnerability_assessment_tools": get_vulnerability_assessment_tools(),
        "enumeration_tools": get_enumeration_tools(),
        "digital_forensic_tools": get_digital_forensic_tools(),
    }
