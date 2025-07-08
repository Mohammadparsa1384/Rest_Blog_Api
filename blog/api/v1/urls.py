from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path , include

app_name = "api-v1"

router = DefaultRouter()
router.register('posts', views.PostViewSet , basename="post")
router.register('category', views.CategoryViewSet, basename="category")
router.register('tags', views.TagViewSet, basename="tag")
router.register("comments", views.CommentViewSet, basename="comment")

urlpatterns = [
    path('', include(router.urls))
]

