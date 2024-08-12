from django.urls import path
from team.views import (
    get_members,
    apply,
    get_applications,
    UpdateMemberImageView,
    ProjectView,
)
from api.views import health_check

urlpatterns = [
    path("members-by-type/", get_members, name="Members_getter"),
    path("apply/", apply, name="Apply"),
    path("applications/", get_applications, name="Applications"),
    path("health-check/", health_check, name="Health_check"),
    path("member/image", UpdateMemberImageView.as_view(), name="Update_member_image"),
    path("projects/", ProjectView.as_view(), name="Projects"),
]
