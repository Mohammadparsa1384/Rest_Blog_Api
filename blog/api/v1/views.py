from rest_framework.viewsets import ModelViewSet
from ...models import Category, Post ,Tag ,  Comment
from .serializers import (PostSerializer, CategorySerialzer, TagSerializer, CommentSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsAuthorOrAdminOrReadOnly
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

class PostViewSet(ModelViewSet):
    """
    ViewSet for managing blog posts.    
    Provides full CRUD functionality.
    
    Access:
    - Admins: full access.
    - Authenticated users: can create posts and see their own drafts.
    - Anonymous users: can only view published posts.

    Supports filtering by status and includes custom logic for visibility of draft posts.
    """
    queryset = Post.objects.all().select_related("category").prefetch_related("tags")
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Post.objects.all()

        if user.is_authenticated:
            return Post.objects.filter(
                Q(status="published") | Q(author=user.profile)
            )

        return Post.objects.filter(status="published")

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

class CategoryViewSet(ModelViewSet):
    """
    ViewSet for managing post categories.

    Provides CRUD operations for blog post categories.
    Accessible by any user. Lookup is based on category slug.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    lookup_field = "slug"

class TagViewSet(ModelViewSet):
    """
    ViewSet for managing post tags.

    Supports CRUD operations for tagging blog posts.
    Accessible by any user. Lookup is based on tag slug.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"

class CommentViewSet(ModelViewSet):
    """
    ViewSet for managing comments on blog posts.

    Features:
    - Only approved comments are visible by default.
    - Admins can see all comments.
    - Authenticated users can create comments.
    - Includes a custom 'approve' action (for admins only).
    - Supports filtering by post, author, and approval status.

    Custom delete response is also implemented.
    """

    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author', 'is_approved']
    
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
        

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({'detail':'Comment approved'})