from rest_framework import serializers
from .models import Member, MemberApplication, ProjectDescription

# Write your serializers here


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class FindMemberSerializer(serializers.Serializer):
    member_type = serializers.CharField(help_text="The category of the member")


class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = ["first_name", "last_name", "email", "phone_number"]

    def create(self, validated_data):
        # Django automatically adds the current date and time for the date_of_application field
        return MemberApplication.objects.create(**validated_data)


class ProjectDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDescription
        fields = "__all__"