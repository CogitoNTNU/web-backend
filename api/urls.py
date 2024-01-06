from django.urls import path
from team.views import get_members, apply

urlpatterns = [
    path("members_by_type/", get_members, name="Members_getter"),
    path("apply/", apply, name="Apply"),
]
