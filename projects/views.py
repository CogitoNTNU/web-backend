from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import newProject
from .serializers import NewProjectSerializer

import sys
from dotenv import load_dotenv
from pathlib import Path

# Assuming `src` is in the `marketing_ai` directory and `views.py` is in the `projects` directory
marketing_ai_path = Path(__file__).resolve().parent / 'marketing_ai'
sys.path.append(str(marketing_ai_path))

from projects.marketing_ai.main import generate_image_from_prompt
env_path = Path(__file__).resolve().parent / 'marketing_ai' / '.env'
load_dotenv(dotenv_path=env_path)

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
    
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def generate_image_view(request):
    """ Generate an image with Marketing AI """
    image_url = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        image_url = generate_image_from_prompt(prompt)  # This function generates the image
        # Save the image to your media directory and create a URL to access it
        image_url = request.build_absolute_uri(image_url)

    return Response(image_url, status=status.HTTP_200_OK)