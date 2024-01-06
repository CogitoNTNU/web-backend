from .models import MemberApplication
from django import forms
from rest_framework import serializers
from .models import Member

# Write your serializers here


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class FindMemberSerializer(serializers.Serializer):
    member_type = serializers.CharField(help_text="The category of the member")


class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = MemberApplication
        fields = ['first_name', 'last_name', 'email', 'phone_number']
