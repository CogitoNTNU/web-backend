from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('members/', include('members.urls'), name="members"),
    path('projects/', include('projects.urls'), name="projects")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
