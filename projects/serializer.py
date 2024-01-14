from rest_framework import serializers


# Write your serializers here

class CreateImageSerializer(serializers.Serializer):
    prompt = serializers.CharField(help_text="The prompt to generate an image from")
    width = serializers.IntegerField(help_text="The width of the image. Width and height must be 1024x1024, 1792x1024, or 1024x1792")
    height = serializers.IntegerField(help_text="The height of the image. Width and height must be 1024x1024, 1792x1024, or 1024x1792")
