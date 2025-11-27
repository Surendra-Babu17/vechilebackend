from rest_framework import serializers
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
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
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
            client.clientPassword = make_password(password)
        client.save()
        return client
