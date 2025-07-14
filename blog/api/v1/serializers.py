from rest_framework import serializers
from accounts.models import Profile
from ...models import (Category, Post, Tag, Comment)
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    
    class Meta:
        model = Profile
        fields = ["id","email"]
        

class CategorySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ["id","title", "slug", "url"]
        extra_kwargs = {
            "url": {
                "view_name": "blog:api-v1:category-detail",
                "lookup_field": "slug",
                
            }
        }

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "slug", "url"]
        extra_kwargs = {
            "url": {
                "view_name": "blog:api-v1:tag-detail",
                "lookup_field": "slug"
            }
        }


class PostSerializer(serializers.ModelSerializer):
    author = serializers.EmailField(source='author.user.email', read_only=True)
    category = CategorySerialzer() 
    category_link = serializers.HyperlinkedRelatedField(
        source="category",
        view_name="blog:api-v1:category-detail",
        lookup_field="slug",
        read_only=True
    )
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field="slug"
    )
    
    class Meta:
        model = Post
        fields = [
            "id", "title",  "author", "slug",
            "category", "category_link", "content",
            "status", "image", "tags", "created_date"
        ]
        read_only_fields = ["id", "author", "slug", "created_date", "updated_date"]
        
    def create(self, validated_data):
        user = self.context['request'].user
        try:
            profile = user.profile 
        except Profile.DoesNotExist:
            raise serializers.ValidationError("User doesn't exists")
        
        validated_data['author'] = profile
        
        category_data = validated_data.pop('category', None)
        if category_data and isinstance(category_data, dict):
            category, _ = Category.objects.get_or_create(**category_data)
            validated_data['category'] = category
        
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(source= 'author.user.email', read_only = True)
    post_title = serializers.CharField(source='post.title', read_only = True)
    class Meta:
        model = Comment
        fields = ["id", "post", "post_title" , "content", "author_email","created_date", "is_approved"]
        read_only_fields = ["id", "created_date", "is_approved", "author_email", "post_title"]