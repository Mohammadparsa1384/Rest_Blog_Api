import pytest
from django.contrib.auth import get_user_model
from accounts.models import Profile
from blog.models import Category, Tag

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