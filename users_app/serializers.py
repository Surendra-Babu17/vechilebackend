from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import userReg, clientReg

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = userReg
        fields = ("userId","userName","email","userPhone","userLocation","password")
        read_only_fields = ("userId",)
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = userReg(**validated_data)
        if password:
            # use model's set_password if available, otherwise fall back to hashing
            if hasattr(user, "set_password"):
                user.set_password(password)
            else:
                user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            if hasattr(instance, "set_password"):
                instance.set_password(password)
            else:
                instance.password = make_password(password)
        instance.save()
        return instance


class ClientRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = clientReg
        fields = ("clientName","clientEmail","clientPhone","clientLocation","clientPassword")
        extra_kwargs = {"clientPassword": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("clientPassword", None)
        client = clientReg(**validated_data)
        if password:
            # if model defines a setter like set_password, prefer it; else hash
            if hasattr(client, "set_password"):
                client.set_password(password)
            else:
                client.clientPassword = make_password(password)
        client.save()
        return client
