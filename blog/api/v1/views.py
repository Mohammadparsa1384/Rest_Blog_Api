from rest_framework.viewsets import ModelViewSet
from ...models import Category, Post ,Tag ,  Comment
from .serializers import (PostSerializer, CategorySerialzer, TagSerializer, CommentSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrAdminOrReadOnly
from rest_framework.response import  Response
from rest_framework import status

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related("category").prefetch_related("tags")
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
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

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all() 
        return Comment.objects.filter(is_approved=True)
    