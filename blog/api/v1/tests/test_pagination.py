from django.urls import reverse
from rest_framework import status

def test_pagination_structure(api_client, bulk_posts):
    url = reverse("blog:api-v1:post-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "pagination" in response.data
    assert "results" in response.data

    pagination = response.data["pagination"]
    assert isinstance(pagination["current_page"], int)
    assert pagination["total_pages"] >= 1
    assert pagination["total_items"] == 15
    assert pagination["next"] is not None or pagination["previous"] is None

    results = response.data["results"]
    assert len(results) == 5  
def test_custom_page_size(api_client, bulk_posts):
    url = reverse("blog:api-v1:post-list") + "?page_size=10"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 10

def test_second_page(api_client, bulk_posts):
    url = reverse("blog:api-v1:post-list") + "?page=2"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    pagination = response.data["pagination"]
    assert pagination["current_page"] == 2
