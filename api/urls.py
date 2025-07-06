from django.urls import path

from api.views import health_check
from team.views import (
    MemberCategoryView,
    UpdateMemberImageView,
    apply,
    get_applications,
    get_members,
)

urlpatterns = [
    path("members-by-type/", get_members, name="Members_getter"),
    path("apply/", apply, name="Apply"),
    path("applications/", get_applications, name="Applications"),
    path("health-check/", health_check, name="Health_check"),
    path("member/image", UpdateMemberImageView.as_view(), name="Update_member_image"),
    path("member/category", MemberCategoryView.as_view(), name="Member_category"),
]
