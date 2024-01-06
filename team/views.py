from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Member
from .serializers import MemberSerializer, FindMemberSerializer
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
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_members(request) -> JsonResponse:
    '''Returns the members wished upon the request'''
    try:
        member_type: str = request.data.get('member_type')
        if (member_type == "Alle Medlemmer"):
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
    description="Sebds",
    examples={"application/json": {"member_type": "Web Developer"}},
)

application_error_response = openapi.Response(
    description="Get the members associated with the 'member_type'",
    examples={"application/json": {"error": "Missing fields"}},
)


@swagger_auto_schema(
    method="POST",
    request_body=FindMemberSerializer,
    operation_description="Sends in an application to Cogito",
    tags=["Member Management"],
    response_description="Returns a message confirming that the application has been registered.",
    responses={200: application_success_response,
               400: application_error_response},
)
@api_view(["POST"])
def apply(request):
    """Apply for membership status to the organization """
    print(request.data, flush=True)
    return None
