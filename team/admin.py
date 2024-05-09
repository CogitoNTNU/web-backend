from django.contrib import admin
from .models import Member, MemberApplication, ProjectDescription, MemberCategory

# Register your models here.
admin.site.register(Member)
admin.site.register(MemberApplication)
admin.site.register(MemberCategory)
admin.site.register(ProjectDescription)
