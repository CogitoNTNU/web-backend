import csv
from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea
from django.utils.html import format_html, format_html_join
from django.http import HttpResponse
from .models import (
    Member,
    MemberApplication,
    Project,
    MemberCategory,
    ProjectMember,
)


class MemberApplicationAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Applicant",
            {
                "fields": (
                    ("first_name", "last_name"),
                    ("email", "phone_number"),
                    "lead",
                )
            },
        ),
        ("Application", {"fields": ("about", "projects_to_join")}),
        ("Timestamps", {"fields": ("date_of_application", "updated_at")}),
    )

    # Read-only system fields
    readonly_fields = ("date_of_application", "updated_at")

    # ---------- list / changelist ----------
    list_display = (
        "full_name",
        "email_link",
        "phone_link",
        "lead",
        "top_three_projects",
        "date_of_application",
    )
    list_display_links = ("full_name",)
    ordering = ("-date_of_application",)
    date_hierarchy = "date_of_application"
    list_per_page = 100

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "about",
        "projects_to_join",  # JSONField cast to text; icontains works on most backends
    )

    list_filter = (("date_of_application", admin.DateFieldListFilter),)

    # Make long text fields nicer to edit
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 6, "style": "width: 100%;"})},
    }

    # Renderers
    @admin.display(description="Name", ordering="last_name")
    def full_name(self, obj: MemberApplication):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description="Email")
    def email_link(self, obj: MemberApplication):
        return format_html('<a href="mailto:{0}">{0}</a>', obj.email)

    @admin.display(description="Phone")
    def phone_link(self, obj: MemberApplication):
        return format_html('<a href="tel:{0}">{0}</a>', obj.phone_number)

    @admin.display(description="Top 3 Projects")
    def top_three_projects(self, obj: MemberApplication):
        if isinstance(obj.projects_to_join, list) and obj.projects_to_join:
            return ", ".join(obj.projects_to_join[:3])
        return "—"

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Pretty print the projects list on the object view:
        replace the default JSON textarea help with an HTML preview below the field.
        """
        response = super().render_change_form(request, context, *args, **kwargs)
        obj = context.get("original")
        if obj and isinstance(obj.projects_to_join, list):
            html_list = format_html(
                "<div style='margin-top:.5rem'><strong>Preview:</strong><ul style='margin:.25rem 0 .5rem 1rem'>{}</ul></div>",
                format_html_join(
                    "", "<li>{}</li>", ((p,) for p in obj.projects_to_join)
                ),
            )
            # Inject a small note shown under the field help
            context["adminform"].form.fields[
                "projects_to_join"
            ].help_text = format_html(
                "{} {}",
                context["adminform"].form.fields["projects_to_join"].help_text,
                html_list,
            )
        return response

    actions = ["export_selected_to_csv"]

    @admin.action(description="Export selected applications to CSV")
    def export_selected_to_csv(self, request, queryset):
        fieldnames = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "lead",
            "date_of_application",
            "updated_at",
            "projects_to_join",
            "about",
        ]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=member_applications.csv"
        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for obj in queryset:
            writer.writerow(
                [
                    obj.first_name,
                    obj.last_name,
                    obj.email,
                    obj.phone_number,
                    obj.lead,
                    obj.date_of_application.isoformat()
                    if obj.date_of_application
                    else "",
                    obj.updated_at.isoformat() if obj.updated_at else "",
                    ", ".join(obj.projects_to_join)
                    if isinstance(obj.projects_to_join, list)
                    else "",
                    (obj.about or "").replace("\n", " ").strip(),
                ]
            )
        return response


# Register your models here.
admin.site.register(Member)
admin.site.register(MemberApplication, MemberApplicationAdmin)
admin.site.register(MemberCategory)
admin.site.register(Project)
admin.site.register(ProjectMember)
