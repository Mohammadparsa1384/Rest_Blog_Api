from django.contrib.auth.models import AnonymousUser
from blog.models import Post


def test_safe_method_allows_anyone(factory, permission, profile_factory):
    request = factory.get("/")  
    request.user = AnonymousUser()
    post = Post(author=profile_factory())  
    assert permission.has_object_permission(request, None, post) is True

def test_author_can_modify_own_post(factory, permission, profile_factory):
    author = profile_factory()
    request = factory.put("/")  
    request.user = author.user
    post = Post(author=author)
    assert permission.has_object_permission(request, None, post) is True

def test_admin_can_modify_any_post(factory, permission, profile_factory, admin_user):
    other_user = profile_factory()
    request = factory.delete("/")  
    request.user = admin_user
    post = Post(author=other_user)
    assert permission.has_object_permission(request, None, post) is True

def test_other_user_cannot_modify_post(factory, permission, profile_factory):
    author = profile_factory(email="author@test.com")
    other_user = profile_factory(email="not-author@test.com")
    request = factory.patch("/")  
    request.user = other_user.user
    post = Post(author=author)
    assert permission.has_object_permission(request, None, post) is False