from digital_forensic.models import DigitalForensicTool


def get_digital_forensic_tools():
    return DigitalForensicTool.objects.all()
