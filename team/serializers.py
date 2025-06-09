from rest_framework import serializers
from .models import Member, MemberApplication, MemberCategory, Project

# Write your serializers here


class MemberSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Member
        fields = "__all__"


class FindMemberSerializer(serializers.Serializer):
    member_type = serializers.CharField(help_text="The category of the member")


class MemberImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())


class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = "__all__"

    def create(self, validated_data):
        # Django automatically adds the current date and time for the date_of_application field
        return MemberApplication.objects.create(**validated_data)


class MemberCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberCategory
        fields = "__all__"


class ProjectDescriptionSerializer(serializers.ModelSerializer):
    leaders = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
