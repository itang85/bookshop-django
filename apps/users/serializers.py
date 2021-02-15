from rest_framework import serializers


class LoginViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
