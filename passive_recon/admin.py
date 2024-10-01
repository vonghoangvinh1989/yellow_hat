from django.contrib import admin
from .models import Tool


# Register your models here.
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tool, ToolAdmin)
