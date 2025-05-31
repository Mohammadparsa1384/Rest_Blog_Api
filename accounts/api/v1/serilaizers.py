from rest_framework import serializers
from ...models import CustomUser , Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistertionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255 , write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirmation password")
    
    class Meta:
        model = User
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
        user = User.objects.create_user(**validated_data, password=password)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['email'] = user.email 
        token['user_id'] = user.id 
        return token
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({'details': 'user is not verified'})
        
        validated_data['user_id'] = self.user.id
        validated_data['email'] = self.user.email
        return validated_data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","first_name", "last_name", "image","bio","created_date","updated_date"]
        read_only_fields = ["id", "created_date", "updated_date"]
        
class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail":"user doesn't exists"})
        
        if user_obj.is_verified:
            raise serializers.ValidationError({"detail":"user is already activate and verified"})
        
        attrs['user_obj'] = user_obj
        return super().validate(attrs)
    
    def get_user(self):
        return self.validated_data.get('user_obj')

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"detail":"password doesn't match"})
        try:
            validate_password(attrs.get("new_password"))
        except ValidationError as e:
            raise serializers.ValidationError({'new_password':list(e.messages)})
        
        return attrs
    
