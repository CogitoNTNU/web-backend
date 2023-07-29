from django.urls import path
from .views import *

urlpatterns = [
    path('all_new_projects/', get_all_new_projects, name="All_new_projects_getter"),
]

