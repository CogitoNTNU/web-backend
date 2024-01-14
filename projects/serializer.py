from rest_framework import serializers


# Write your serializers here

class CreateImageSerializer(serializers.Serializer):
    prompt = serializers.CharField(help_text="The prompt to generate an image from")
    width = serializers.IntegerField(help_text="The width of the image")
    height = serializers.IntegerField(help_text="The height of the image")
