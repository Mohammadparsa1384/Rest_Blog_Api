from django.urls import reverse
from rest_framework import status

class TestPostAPI:
    def test_list_posts(self, api_client, published_post):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_detail(self, api_client, published_post):
        url = reverse("blog:api-v1:post-detail", kwargs={"slug": published_post.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


class TestCategoryAPI:
    def test_list_categories(self, api_client, category):
        url = reverse("blog:api-v1:category-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_category_detail(self, api_client, category):
        url = reverse("blog:api-v1:category-detail", kwargs={"slug": category.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


class TestTagAPI:
    def test_list_tags(self, api_client, tag):
        url = reverse("blog:api-v1:tag-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_tag_detail(self, api_client, tag):
        url = reverse("blog:api-v1:tag-detail", kwargs={"slug": tag.slug})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


class TestCommentAPI:
    def test_list_comments(self, api_client, approved_comment):
        url = reverse("blog:api-v1:comment-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_comment_detail(self, api_client, approved_comment):
        url = reverse("blog:api-v1:comment-detail", kwargs={"pk": approved_comment.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
