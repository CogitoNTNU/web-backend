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


class MemberImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())


class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = "__all__"

    def create(self, validated_data):
        # Django automatically adds the current date and time for the date_of_application field
        return MemberApplication.objects.create(**validated_data)


class ProjectDescriptionSerializer(serializers.ModelSerializer):
    leaders = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,  # This field is only for input, not part of the output
    )

    class Meta:
        model = ProjectDescription
        fields = "__all__"

    def create(self, validated_data):
        # Extract leaders emails
        leader_emails = validated_data.pop("leaders", [])

        # Create the project
        project = ProjectDescription.objects.create(**validated_data)

        # Query the Member objects and add them to the project's leaders
        leaders = Member.objects.filter(email__in=leader_emails)
        project.leaders.set(leaders)

        return project

    def to_representation(self, instance):
        """Convert the model instance to the expected output format."""
        representation = super().to_representation(instance)
        # Add leader emails in the representation
        representation["leaders"] = list(
            instance.leaders.values_list("email", flat=True)
        )
        return representation
