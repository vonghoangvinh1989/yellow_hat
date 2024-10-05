from django.contrib import admin
from .models import ActiveReconTool


class ActiveReconToolAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


# Register your models here.
admin.site.register(ActiveReconTool, ActiveReconToolAdmin)
