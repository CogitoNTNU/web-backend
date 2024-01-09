from django.urls import path
from team.views import get_members, apply, get_applications, get_projects_descriptions, add_project_description

urlpatterns = [
    path("members_by_type/", get_members, name="Members_getter"),
    path("apply/", apply, name="Apply"),
    path("applications/", get_applications, name="Applications"),
]
