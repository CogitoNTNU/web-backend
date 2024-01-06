from django.urls import path
from .views import *
urlpatterns = [
    path('members_by_type/', get_members, name="Members_getter")]
