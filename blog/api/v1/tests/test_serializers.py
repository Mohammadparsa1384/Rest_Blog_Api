import pytest
from django.contrib.auth import get_user_model
from accounts.models import Profile
from blog.models import Category, Tag, Post, Comment
from blog.api.v1.serializers import (
    ProfileSerializer,
    CategorySerialzer,
    TagSerializer,
    PostSerializer,
    CommentSerializer
)
from rest_framework.test import APIRequestFactory

def test_profile_serializer_serialization(profile_factory):
    profile = profile_factory(email="ali@example.com")
    serializer = ProfileSerializer(instance=profile)
    data = serializer.data
    assert data["email"] == profile.user.email


def test_category_serializer_serialization(category):
    request = APIRequestFactory().get("/")
    serializer = CategorySerialzer(instance=category, context={"request": request})
    data = serializer.data
    assert data["title"] == "Django"
    assert "url" in data


def test_tag_serializer_serialization(tag):
    request = APIRequestFactory().get("/")
    serializer = TagSerializer(instance=tag, context={"request": request})
    data = serializer.data
    assert data["slug"] == "python"
    assert "url" in data


def test_post_serializer_create(profile_factory, category, tag):
    profile = profile_factory(email="ahmad@example.com")
    user = profile.user

    data = {
        "title": "Test Post",
        "content": "Some content here",
        "status": "published",
        "category": {
            "title": category.title,
            "slug": category.slug
        },
        "tags": [tag.slug],
    }

    request = APIRequestFactory().post("/")
    request.user = user
    serializer = PostSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()
    assert post.author == profile
    assert post.title == "Test Post"


def test_comment_serializer_serialization(profile_factory, category, tag):
    profile = profile_factory(email="commentuser@example.com")
    post = Post.objects.create(
        title="Some post",
        slug="some-post",
        content="Content",
        status="published",
        category=category,
        author=profile,
    )
    comment = Comment.objects.create(
        post=post,
        content="Nice post!",
        author=profile,
    )
    serializer = CommentSerializer(instance=comment)
    data = serializer.data
    assert data["author_email"] == profile.user.email
    assert data["post_title"] == post.title
    assert data["content"] == "Nice post!"
