from django.contrib import admin
from .models import Member, MemberApplication, Project

# Register your models here.
admin.site.register(Member)
admin.site.register(MemberApplication)

admin.site.register(ProjectDescription)