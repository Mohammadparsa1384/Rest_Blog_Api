import pytest
from django.contrib.auth import get_user_model
from accounts.models import Profile
from blog.models import (Category, Post, Tag, Comment)
from rest_framework.test import APIClient , APIRequestFactory
from ..permissions import IsAuthorOrAdminOrReadOnly

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
def api_client():
    return APIClient()

@pytest.fixture
def published_post(profile_factory, category):
    return Post.objects.create(
        title="Published Post",
        slug="published-post",
        content="Content",
        status="published",
        category=category,
        author=profile_factory(email="pub@example.com")
    )

@pytest.fixture
def draft_post(profile_factory, category):
    return Post.objects.create(
        title="Draft Post",
        slug="draft-post",
        content="Draft content",
        status="draft",
        category=category,
        author=profile_factory(email="draft_user@example.com")
    )

@pytest.fixture
def category(db):
    return Category.objects.create(title="Django", slug="django")

@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Python", slug="python")

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(profile_factory):
    user = profile_factory(email="auth@example.com").user
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def post(profile_factory, category):
    return Post.objects.create(
        title="Post for comments",
        slug="post-comments",
        content="...",
        status="published",
        category=category,
        author=profile_factory().user.profile,
    )

@pytest.fixture
def approved_comment(profile_factory, post):
    return Comment.objects.create(
        post=post,
        content="Approved",
        author=profile_factory(email="approved@example.com"),
        is_approved=True,
    )

@pytest.fixture
def unapproved_comment(profile_factory, post):
    return Comment.objects.create(
        post=post,
        content="Not approved yet",
        author=profile_factory(email="pending@example.com"),
        is_approved=False,
    )

@pytest.fixture
def comment_by_user(profile_factory, post):
    profile = profile_factory(email="owner@example.com")
    return Comment.objects.create(
        post=post,
        content="User comment",
        author=profile,
        is_approved=False,
    )

@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(email="admin@example.com", password="admin123")


@pytest.fixture
def permission():
    return IsAuthorOrAdminOrReadOnly()

@pytest.fixture
def factory():
    return APIRequestFactory()

@pytest.fixture
def bulk_posts(profile_factory, category):
    author = profile_factory(email="pagetest@example.com")
    return [
        Post.objects.create(
            title=f"Post {i}",
            slug=f"post-{i}",
            content="Test content",
            status="published",
            category=category,
            author=author
        )
        for i in range(15)
    ]
