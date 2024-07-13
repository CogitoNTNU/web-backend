from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from .models import Member, MemberApplication, ProjectDescription
from .serializers import (
    MemberImageUploadSerializer,
    MemberSerializer,
    FindMemberSerializer,
    MemberApplicationSerializer,
    ProjectDescriptionSerializer,
)
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Get member view
member_success_response = openapi.Response(
    description="Get the members associated with the 'member_type'",
    examples={"application/json": {"member_type": "Web Developer"}},
)

member_error_response = openapi.Response(
    description="Get the members associated with the 'member_type'",
    examples={"application/json": {"error": "Missing fields"}},
)


@swagger_auto_schema(
    method="GET",
    query_serializer=FindMemberSerializer,
    operation_description="Get members with the specified category, for retrieval of all members set it to 'Alle Medlemmer' ",
    tags=["Member Management"],
    response_description="Returns the members wished upon the request",
    responses={200: member_success_response, 400: member_error_response},
)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_members(request) -> JsonResponse:
    """Returns the members wished upon the request"""
    try:
        member_type: str = request.query_params.get("member_type")
        if member_type == "Alle Medlemmer":
            members = Member.objects.all()
        else:
            members = Member.objects.filter(category__title=member_type)
        serializer = MemberSerializer(members, many=True)

        return JsonResponse(serializer.data, safe=False)

    except Exception as e:
        response = {"error": e}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class UpdateMemberImageView(APIView):

    @swagger_auto_schema(
        operation_description="Update the image of a member",
        tags=["Member Management"],
        request_body=MemberImageUploadSerializer,
        responses={200: "Success", 400: "Bad Request"},
    )
    def post(self, request, *args, **kwargs):
        serializer = MemberImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            images = serializer.validated_data["images"]
            updated_members = []
            members_not_found = []

            for image in images:
                # Extract member name from image file name (assuming 'FirstName_LastName.ext')
                member_name = image.name.rsplit(".", 1)[0]

                try:
                    member = Member.objects.get(name=member_name)
                    member.image = image
                    member.save()
                    updated_members.append(member)
                except Member.DoesNotExist:
                    members_not_found.append(member_name)
                    continue

            response = {
                "updated_members": MemberSerializer(updated_members, many=True).data,
                "members_not_found": members_not_found,
            }
            return Response(
                response,
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Apply
application_success_response = openapi.Response(
    description="Sends an application for membership to Cogito",
    examples={"application/json": {"member_type": "Web Developer"}},
)

application_error_response = openapi.Response(
    description="The application was not sent in due to missing fields or invalid data",
    examples={"application/json": {"error": "Missing fields"}},
)


@swagger_auto_schema(
    method="POST",
    request_body=MemberApplicationSerializer,
    operation_description="Sends in an application to Cogito",
    tags=["Member Management"],
    response_description="Returns a message confirming that the application has been registered.",
    responses={200: application_success_response, 400: application_error_response},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def apply(request):
    """Apply for membership status to the organization"""

    serializer = MemberApplicationSerializer(data=request.data)
    if serializer.is_valid():
        application: MemberApplication = serializer.save()

        # Send confirmation email
        subject = "Application Received by Cogito NTNU"
        message = f"""Dear {application.first_name} {application.last_name},\n\nThank you for your application. We have received your details and our team will send you future details on Email and/or Phone. \nIf you have any questions, please feel free to contact us at: styre@cogito-ntnu.no\n\nBest regards,\nCogito NTNU """
        recipient_list = [application.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        message = {"message": "Application sent in successfully"}
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get applications
application_success_response = openapi.Response(
    description="Get all applications",
    examples={
        "application/json": [
            {
                "first_name": "FIRST_NAME_OF_APPLICANT",
                "last_name": "SECOND_NAME_OF_APPLICANT",
                "email": "user@example.com",
                "about": "My name is FIRST_NAME and my last name is SECOND_NAME",
                "phone_number": "12345678",
            }
        ]
    },
)


@swagger_auto_schema(
    method="GET",
    operation_description="Get all applications",
    tags=["Member Management"],
    response_description="Returns all applications",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_applications(request):
    """Returns all applications"""
    applications = MemberApplication.objects.all()
    serializer = MemberApplicationSerializer(applications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get Projects
project_success_response = openapi.Response(
    description="Get all projects",
    examples={
        "application/json": [
            {
                "name": "Project Name",
                "description": "Project Description",
                "image": "Image",
                "github": "GitHub",
                "website": "Website",
            }
        ]
    },
)


@swagger_auto_schema(
    method="GET",
    operation_description="Get all projects",
    tags=["Project Management"],
    response_description="Returns all projects",
    response={200: project_success_response},
)
@api_view(["GET"])
def get_projects_descriptions(request):
    """Returns all projects"""
    projects = ProjectDescription.objects.all()
    serializer = ProjectDescriptionSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Add Project
project_success_response = openapi.Response(
    description="Add a project",
    examples={
        "application/json": {
            "message": "Project added successfully",
        }
    },
)
project_error_response = openapi.Response(
    description="The project was not added due to missing fields or invalid data",
    examples={"application/json": {"error": "Missing fields"}},
)


@swagger_auto_schema(
    method="POST",
    operation_description="Add a project description",
    tags=["Project Management"],
    response_description="Returns a message confirming that the project has been added.",
    responses={200: project_success_response, 400: project_error_response},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_project_description(request):
    """Add a project"""
    serializer = ProjectDescriptionSerializer(data=request.data)
    if serializer.is_valid():
        # Check if the leaders are valid members
        leader_emails = request.data.get("leaders", [])
        for email in leader_emails:
            if not Member.objects.filter(email=email).exists():
                message = {
                    "error": f"Invalid leader member, member {email} does not exist"
                }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

        project = serializer.save()

        # Associate leaders
        for email in leader_emails:
            leader = Member.objects.get(email=email)
            project.leaders.add(leader)
        message = {"message": "Project description added successfully"}
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
