from rest_framework import serializers
from ...models import CustomUser , Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegistertionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255 , write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirmation password")
    
    class Meta:
        model = CustomUser
        fields = ["email","password","password2"]
        
    def validate(self, attrs):
        if attrs['password'] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user