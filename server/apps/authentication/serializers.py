from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'name', 'tagline', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.tagline = validated_data.get('tagline', instance.tagline)

        instance.save()

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.is_active = True
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance

    def to_representation(self, obj):
        data = super(AccountSerializer, self).to_representation(obj)

        return data


class LoginCustomSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200)


class PasswordCustomSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)

