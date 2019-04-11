from django.contrib.auth import authenticate
from rest_framework import serializers
from lunchorderingapp.mixins import UserSerializer
from . import models


class LoginSerializer(UserSerializer, serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = (
            'email',
            'password'
            )

    def validate(self, data):
        user = authenticate(
            self.context['request'],
            email=data.get('email'),
            password=data.get('password'),
        )
        
        if not user:
        	print(user)
        else:
        	print(user)

        self.user = user

        return data


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= models.Product
        
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= models.Order
        
        fields = ('product_id',)

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super(OrderSerializer, self).create(validated_data)