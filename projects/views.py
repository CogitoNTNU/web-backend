from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import sys
from dotenv import load_dotenv
from pathlib import Path

# Assuming `src` is in the `MarketingAI` directory and `views.py` is in the `projects` directory
marketing_ai_path = Path(__file__).resolve().parent / 'marketing_ai'
sys.path.append(str(marketing_ai_path))

from projects.marketing_ai.main import generate_image_from_prompt
env_path = Path(__file__).resolve().parent / 'marketing_ai' / '.env'
print(f"env_path: {env_path}", flush=True)
load_dotenv(dotenv_path=env_path)

request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['prompt'],
    properties={
        'prompt': openapi.Schema(type=openapi.TYPE_STRING, description='The prompt to generate an image from'),
    },
)

@swagger_auto_schema(
    method="POST",
    request_body=request_body,
    operation_description="Generate an image with Marketing AI",
    tags=["Marketing AI"],
    response_description="Returns the image url",
    responses={200: "Image url", 400: "Error"},
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def generate_image_view(request):
    """ Generate an image with Marketing AI """
    image_url = None
    if request.method == 'POST':
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({"error": "No prompt provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"The prompt the user gave was: {prompt}")
        image_url, new_prompt = generate_image_from_prompt(prompt)  # This function generates the image
        # Save the image to your media directory and create a URL to access it
        # image_url = request.build_absolute_uri(image_url)
        data = {
            "image_url": image_url,
            "prompt": new_prompt,
        }
    return Response(data, status=status.HTTP_200_OK)