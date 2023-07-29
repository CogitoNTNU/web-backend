from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import newProject
from .serializers import NewProjectSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_new_projects(request):
    '''
    Returns all the new projects in the database.
    '''
    try:
        projects = newProject.objects.all()
        serializer = NewProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)