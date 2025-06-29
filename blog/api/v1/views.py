from rest_framework.viewsets import ModelViewSet
from ...models import Category, Post ,Tag
from .serializers import (PostSerializer, CategorySerialzer, TagSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related("category").prefetch_related("tags")
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    lookup_field = "slug"

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    