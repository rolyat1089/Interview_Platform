
from rest_framework import serializers
from interviewQuiz.models import  InterviewTest,  InterviewTestAttempt
from login.serializers import UserSerializer
from django.core.validators import MaxValueValidator

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTest
        fields = ['id', 'DisplayTime', 'EndTime', 'Title', 'Instructions', 'TestTime',]


class InterviewTestAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTestAttempt
        fields = ['Test', 'StartTime', 'Attempted', 'Finished']

class TestSerializerAdmin(serializers.ModelSerializer):
    accounts = UserSerializer(many = True)
    class Meta:
        model = InterviewTest
        fields = ['id', 'DisplayTime', 'EndTime', 'Title', 'Instructions', 'TestTime','accounts']


class TestInputSerializer(serializers.Serializer):
    test_id = serializers.IntegerField(required = True, validators = [MaxValueValidator(5000)])

class TestDataSerializer(serializers.Serializer):
    display_time = serializers.DateTimeField(required = True)
    end_time = serializers.DateTimeField(required = True)
    title = serializers.CharField(required = True)
    instructions = serializers.CharField(required = True)
    test_time = serializers.IntegerField(required = True)
    


        