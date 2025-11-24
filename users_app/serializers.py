from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import userReg, clientReg

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = userReg
        fields = ("userId","userName","email","userPhone","userLocation","password")
        read_only_fields = ("userId",)
        extra_kwargs = {
            "password": {"write_only": True}  # write only
        }

    def create(self, validated_data):
        pwd = validated_data.get("password")
        if pwd:
            validated_data["password"] = make_password(pwd)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            pwd = validated_data.get("password")
            if pwd:
                validated_data["password"] = make_password(pwd)
        return super().update(instance, validated_data)


class ClientRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = clientReg
        fields = ("clientName","clientEmail","clientPhone","clientLocation","clientPassword")
        extra_kwargs = {
            "clientPassword": {"write_only": True}
        }

    def create(self, validated_data):
        pwd = validated_data.get("clientPassword")
        if pwd:
            validated_data["clientPassword"] = make_password(pwd)
        return super().create(validated_data)
