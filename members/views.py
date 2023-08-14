from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Member
from .serializers import MemberSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_members(request):
    '''
    Returns all the members in the database.
    '''
    try:
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_lead_members(request):
    '''
    Returns all the members in the database.
    '''
    try:
        members = Member.objects.filter(category="Lead")
        serializer = MemberSerializer(members, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_web_members(request):
    '''
    Returns all the members in the database.
    '''
    try:
        members = Member.objects.filter(category="Web")
        serializer = MemberSerializer(members, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_HR_members(request):
    '''
    Returns all the members in the database.
    '''
    try:
        members = Member.objects.filter(category="HR")
        serializer = MemberSerializer(members, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_Healthcheck(request):
    '''
    Returns a healthcheck
    '''
    return Response(status=status.HTTP_200_OK)
        