from django.urls import path
from team.views import get_members

urlpatterns = [path("members_by_type/", get_members, name="Members_getter")]
