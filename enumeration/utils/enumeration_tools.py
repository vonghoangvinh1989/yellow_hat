from enumeration.models import EnumerationTool


def get_enumeration_tools():
    return EnumerationTool.objects.all()
