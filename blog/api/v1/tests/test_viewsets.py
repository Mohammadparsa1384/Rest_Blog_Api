import pytest
from django.urls import reverse
from rest_framework import status
from blog.models import (Post , Category, Tag)


class TestPostViewSet:

    def test_anonymous_user_can_see_published_posts(self, api_client, published_post):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(post["slug"] == published_post.slug for post in response.data["results"])

    def test_authenticated_user_can_see_own_drafts(self, api_client, draft_post):
        user = draft_post.author.user
        api_client.force_authenticate(user=user)
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(post["slug"] == draft_post.slug for post in response.data["results"])

    def test_user_cannot_see_others_drafts(self, api_client, draft_post, profile_factory):
        other_user = profile_factory(email="other@example.com").user
        api_client.force_authenticate(user=other_user)
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert all(post["slug"] != draft_post.slug for post in response.data["results"])

    def test_authenticated_user_can_create_post(self, api_client, profile_factory, category, tag):
        user = profile_factory(email="creator@example.com").user
        api_client.force_authenticate(user=user)

        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "My New Post",
            "content": "Hello World!",
            "status": "published",
            "category": {
                "title": category.title,
                "slug": category.slug
            },
            "tags": [tag.slug],
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "My New Post"

    def test_author_can_delete_own_post(self, api_client, published_post):
        user = published_post.author.user
        api_client.force_authenticate(user=user)
        url = reverse("blog:api-v1:post-detail", kwargs={"slug": published_post.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_filter_by_status(self, api_client, published_post, draft_post):
        url = reverse("blog:api-v1:post-list") + "?status=published"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert all(post["status"] == "published" for post in response.data["results"])

    def test_search_by_title(self, api_client, published_post):
        url = reverse("blog:api-v1:post-list") + "?search=Published"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any("Published" in post["title"] for post in response.data["results"])



class TestCategoryViewSet:

    def test_list_categories(self, api_client, category):
        url = reverse("blog:api-v1:category-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(cat["slug"] == category.slug for cat in response.data['results'])

    def test_retrieve_category(self, api_client, category):
        url = reverse("blog:api-v1:category-detail", kwargs={"slug": category.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == category.title

    def test_create_category(self, authenticated_client):
        url = reverse("blog:api-v1:category-list")
        data = {"title": "Frontend", "slug": "frontend"}
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(slug="frontend").exists()

    def test_update_category(self, authenticated_client, category):
        url = reverse("blog:api-v1:category-detail", kwargs={"slug": category.slug})
        data = {"title": "Updated Title", "slug": category.slug}
        response = authenticated_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.title == "Updated Title"

    def test_delete_category(self, authenticated_client, category):
        url = reverse("blog:api-v1:category-detail", kwargs={"slug": category.slug})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(slug=category.slug).exists()


class TestTagViewSet:

    def test_list_tags(self, api_client, tag):
        url = reverse("blog:api-v1:tag-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(t["slug"] == tag.slug for t in response.data['results'])

    def test_retrieve_tag(self, api_client, tag):
        url = reverse("blog:api-v1:tag-detail", kwargs={"slug": tag.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == tag.name

    def test_create_tag(self, authenticated_client):
        url = reverse("blog:api-v1:tag-list")
        data = {"name": "Python", "slug": "python"}
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Tag.objects.filter(slug="python").exists()

    def test_update_tag(self, authenticated_client, tag):
        url = reverse("blog:api-v1:tag-detail", kwargs={"slug": tag.slug})
        data = {"name": "Updated Tag", "slug": tag.slug}
        response = authenticated_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        tag.refresh_from_db()
        assert tag.name == "Updated Tag"

    def test_delete_tag(self, authenticated_client, tag):
        url = reverse("blog:api-v1:tag-detail", kwargs={"slug": tag.slug})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Tag.objects.filter(slug=tag.slug).exists()


class TestCommentViewSet:

    def test_only_approved_comments_visible_to_anonymous(self, api_client, approved_comment, unapproved_comment):
        url = reverse("blog:api-v1:comment-list")
        response = api_client.get(url)
        assert response.status_code == 200
        comment_ids  = [comment["id"] for comment in response.data['results']]
        assert approved_comment.id in comment_ids 
        assert unapproved_comment.id not in comment_ids 

    def test_admin_can_see_all_comments(self, api_client, admin_user, approved_comment, unapproved_comment):
        api_client.force_authenticate(user=admin_user)
        url = reverse("blog:api-v1:comment-list")
        response = api_client.get(url)
        ids = [comment["id"] for comment in response.data['results']]
        assert approved_comment.id in ids
        assert unapproved_comment.id in ids

    def test_authenticated_user_can_create_comment(self, api_client, profile_factory, post):
        user = profile_factory(email="user@example.com").user
        api_client.force_authenticate(user=user)
        url = reverse("blog:api-v1:comment-list")
        data = {
            "post": post.id,
            "content": "Great post!",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert response.data["content"] == "Great post!"

    def test_anonymous_user_cannot_create_comment(self, api_client, post):
        url = reverse("blog:api-v1:comment-list")
        data = {
            "post": post.id,
            "content": "Trying anonymously",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_author_can_delete_own_comment(self, api_client, comment_by_user):
        user = comment_by_user.author.user
        api_client.force_authenticate(user=user)
        url = reverse("blog:api-v1:comment-detail", kwargs={"pk": comment_by_user.id})
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_admin_can_approve_comment(self, api_client, admin_user, unapproved_comment):
        api_client.force_authenticate(user=admin_user)
        url = reverse("blog:api-v1:comment-approve", kwargs={"pk": unapproved_comment.id})
        response = api_client.post(url)
        assert response.status_code == 200
        unapproved_comment.refresh_from_db()
        assert unapproved_comment.is_approved is True

    def test_filter_by_post(self, api_client, approved_comment):
        url = reverse("blog:api-v1:comment-list") + f"?post={approved_comment.post.id}"
        response = api_client.get(url)
        assert response.status_code == 200
        assert all(comment["post"] == approved_comment.post.id for comment in response.data['results'])