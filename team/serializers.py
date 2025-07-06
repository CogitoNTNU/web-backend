from rest_framework import serializers

from .models import Member, MemberApplication, MemberCategory, Project, ProjectMember


class ProjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "logo", "hours_a_week", "github_link")


class ProjectMemberSerializer(serializers.ModelSerializer):
    project = ProjectBriefSerializer(read_only=True)
    semester = serializers.CharField(source="get_semester_display", read_only=True)

    class Meta:
        model = ProjectMember
        fields = (
            "project",
            "role",
            "year",
            "semester",
        )


class MemberSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    project_memberships = ProjectMemberSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Member
        fields = "__all__"


class FindMemberSerializer(serializers.Serializer):
    member_type = serializers.CharField()


class MemberImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())


class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = "__all__"

    def create(self, validated_data):
        return MemberApplication.objects.create(**validated_data)


class MemberCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberCategory
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    leaders = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
