from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Member, MemberApplication
from .serializers import (
    MemberSerializer,
    FindMemberSerializer,
    MemberApplicationSerializer,
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
    method="POST",
    request_body=FindMemberSerializer,
    operation_description="Get members",
    tags=["Member Management"],
    response_description="",
    responses={200: member_success_response, 400: member_error_response},
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_members(request) -> JsonResponse:
    """Returns the members wished upon the request"""
    try:
        member_type: str = request.data.get("member_type")
        if member_type == "Alle Medlemmer":
            members = Member.objects.all()
        else:
            members = Member.objects.filter(category=member_type)
        serializer = MemberSerializer(members, many=True)

        return JsonResponse(serializer.data, safe=False)

    except Exception as e:
        response = {"error": e}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


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
        serializer.save()
        message = {"message": "Application sent in successfully"}
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
