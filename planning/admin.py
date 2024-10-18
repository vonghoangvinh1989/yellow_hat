from django.contrib import admin
from .models import PenetrationTest


@admin.register(PenetrationTest)
class PenetrationTestAdmin(admin.ModelAdmin):
    list_display = (
        "team_primary_contact",
        "team_primary_phone",
        "target_primary_contact",
        "start_date",
        "end_date",
        "black_box",
    )
    search_fields = (
        "team_primary_contact",
        "target_primary_contact",
        "attack_ips",
    )
    list_filter = (
        "black_box",
        "announced_test",
        "shun_ip",
        "conclude_test",
    )
    ordering = ("start_date",)
    date_hierarchy = "start_date"
    list_per_page = 20

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "team_primary_contact",
                    "team_primary_phone",
                    "team_primary_pager",
                    "team_secondary_contact",
                    "team_secondary_phone",
                    "team_secondary_pager",
                )
            },
        ),
        (
            "Target Organization",
            {
                "fields": (
                    "target_primary_contact",
                    "target_primary_phone",
                    "target_primary_pager",
                    "target_secondary_contact",
                    "target_secondary_phone",
                    "target_secondary_pager",
                )
            },
        ),
        (
            "Testing Information",
            {
                "fields": (
                    "debrief_frequency",
                    "debrief_location",
                    "start_date",
                    "end_date",
                    "test_times",
                    "announced_test",
                    "shun_ip",
                    "automatic_shun",
                    "shun_steps",
                    "conclude_test",
                    "continue_test",
                    "attack_ips",
                    "black_box",
                    "viewing_policy",
                    "observing_team",
                )
            },
        ),
        (
            "Signatures",
            {
                "fields": (
                    "target_signature",
                    "target_date",
                    "pen_test_leader",
                    "leader_date",
                    "tester_signatures",
                    "target_signature_image",  # New field for target signature image
                    "pen_test_leader_signature_image",  # New field for pen test leader signature image
                )
            },
        ),
    )

    # Customize how the image fields are displayed in the admin list view
    def target_signature_image_display(self, obj):
        if obj.target_signature_image:
            return (
                f'<img src="{obj.target_signature_image.url}" width="100" height="50"/>'
            )
        return "No image"

    target_signature_image_display.allow_tags = True

    def pen_test_leader_signature_image_display(self, obj):
        if obj.pen_test_leader_signature_image:
            return f'<img src="{obj.pen_test_leader_signature_image.url}" width="100" height="50"/>'
        return "No image"

    pen_test_leader_signature_image_display.allow_tags = True

    # Add these fields to list_display to see images in the admin list view
    list_display = list_display + (
        "target_signature_image_display",
        "pen_test_leader_signature_image_display",
    )
