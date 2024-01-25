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
from projects.models import Image

from projects.serializer import CreateImageSerializer

# Assuming `src` is in the `MarketingAI` directory and `views.py` is in the `projects` directory
marketing_ai_path = Path(__file__).resolve().parent / "marketing_ai"
sys.path.append(str(marketing_ai_path))

from projects.marketing_ai.main import generate_image_from_prompt

env_path = Path(__file__).resolve().parent / "marketing_ai" / ".env"
print(f"env_path: {env_path}", flush=True)
load_dotenv(dotenv_path=env_path)


@swagger_auto_schema(
    method="POST",
    request_body=CreateImageSerializer,
    operation_description="Generate an image with Marketing AI",
    tags=["Marketing AI"],
    response_description="Returns the image url",
    responses={200: "Image url", 400: "Error"},
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def generate_image_view(request):
    """Generate an image with Marketing AI"""
    serializer = CreateImageSerializer(data=request.data)
    if serializer.is_valid():
        prompt = serializer.validated_data.get("prompt")

        width = serializer.validated_data.get("width")
        height = serializer.validated_data.get("height")
        # Check 1024x1024, 1792x1024, or 1024x1792
        if (
            not (height == 1024 and width == 1024)
            and not (width == 1024 and height == 1792)
            and not (width == 1792 and height == 1024)
        ):
            return Response(
                {"error": "Invalid image size"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not prompt:
            return Response(
                {"error": "No prompt provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        print(f"The prompt the user gave was: {prompt}")
        image_url, new_prompt = generate_image_from_prompt(
            prompt, width=width, height=height
        )  # This function generates the image

        data = {
            "image_url": image_url,
            "prompt": new_prompt,
        }
        # save the image to the database
        # Image.objects.create(
        #     image_url=image_url, prompt=new_prompt, height=height, width=width
        # )

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="GET",
    operation_description="Get all the images from the database",
    tags=["Marketing AI"],
    response_description="Returns all the images",
    responses={200: "Images", 400: "Error"},
)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_images(request):
    """Get all the images from the database"""
    images = Image.objects.all()
    data = []
    for image in images:
        data.append(
            {
                "image_url": image.image_url,
                "prompt": image.prompt,
                "date_of_generation": image.date_of_generation,
                "height": image.height,
                "width": image.width,
            }
        )
    return Response(data, status=status.HTTP_200_OK)
