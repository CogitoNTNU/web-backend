from django.urls import path
from .views import *
urlpatterns = [
    path('all_members/', get_all_members, name="All_members_getter"),
    path('lead_members/', get_lead_members, name="Lead_members_getter"),
    path('web_members/', get_web_members, name="Web_members_getter"),
    path('hr_members/', get_HR_members, name="HR_members_getter"),
]

