from rest_framework import serializers
from .models import newProject

class NewProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = newProject
        fields = '__all__'

