from django.urls import path
from team.views import (
    get_members,
    apply,
    get_applications,
    get_projects_descriptions,
    add_project_description,
)
from .views import health_check

urlpatterns = [
    path("members_by_type/", get_members, name="Members_getter"),
    path("apply/", apply, name="Apply"),
    path("applications/", get_applications, name="Applications"),
    path("health-check/", health_check, name="Health_check"),
    path(
        "projects-description/", get_projects_descriptions, name="Project_description"
    ),
    path(
        "add-project-description/",
        add_project_description,
        name="Add_project_description",
    ),
]
