from django.urls import path
from projects.views import generate_image_view, get_images
from team.views import (
    get_members,
    apply,
    get_applications,
)
from api.views import health_check

urlpatterns = [
    path("members-by-type/", get_members, name="Members_getter"),
    path("apply/", apply, name="Apply"),
    path("applications/", get_applications, name="Applications"),
    path("health-check/", health_check, name="Health_check"),
    path("projects/marketing-ai/", generate_image_view, name="Generate_image"),
    path("projects/marketing-ai/images", get_images, name="Get_images"),
]
