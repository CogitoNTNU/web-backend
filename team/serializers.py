from rest_framework import serializers
from .models import Member, MemberApplication, ProjectDescription

# Write your serializers here


class MemberSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Member
        fields = "__all__"


class FindMemberSerializer(serializers.Serializer):
    member_type = serializers.CharField(help_text="The category of the member")


class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = "__all__"

    def create(self, validated_data):
        # Django automatically adds the current date and time for the date_of_application field
        return MemberApplication.objects.create(**validated_data)


class ProjectDescriptionSerializer(serializers.ModelSerializer):
    # List of strings
    leader_emails = serializers.ListSerializer(
        child=serializers.EmailField(), write_only=True
    )

    class Meta:
        model = ProjectDescription
        fields = [
            "name",
            "description",
            "image",
            "hours_a_week",
            "github",
            "website",
            "leader_emails",
        ]
