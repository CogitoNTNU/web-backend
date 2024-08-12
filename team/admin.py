from django.contrib import admin
from .models import (
    Member,
    MemberApplication,
    ProjectDescription,
    MemberCategory,
)


class MemberApplicationAdmin(admin.ModelAdmin):
    # Fields to be displayed in the admin panel even they are read-only
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "about",
        "date_of_application",
        "projects_to_join",
    ]
    # Fields that are read-only in the admin panel
    readonly_fields = [
        "date_of_application",
    ]


# Register your models here.
admin.site.register(Member)
admin.site.register(MemberApplication, MemberApplicationAdmin)
admin.site.register(MemberCategory)
admin.site.register(ProjectDescription)
