from django.contrib import admin
from .models import DigitalForensicTool


# Register your models here.
class DigitalForensicToolAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


# Register your models here.
admin.site.register(DigitalForensicTool, DigitalForensicToolAdmin)
