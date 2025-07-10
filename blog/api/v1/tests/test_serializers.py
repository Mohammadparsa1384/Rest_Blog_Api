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

# -------------------
# Fixtures
# -------------------

@pytest.fixture
def user_factory(db):
    def create_user(email="parsajavidi@gmail.com"):
        return get_user_model().objects.create_user(email=email, password="test1234")
    return create_user

@pytest.fixture
def profile_factory(user_factory):
    def create_profile(email="parsajavidi@gmail.com"):
        user = user_factory(email=email)
        profile, created = Profile.objects.get_or_create(user=user, defaults={
            "first_name": "parsa",
            "last_name": "javidi",
        })
        return profile
    return create_profile

@pytest.fixture
def category(db):
    return Category.objects.create(title="Django", slug="django")

@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Python", slug="python")

# -------------------
# Tests
# -------------------

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
