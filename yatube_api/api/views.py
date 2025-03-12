from rest_framework import viewsets, serializers
from posts.models import Post, Group, Follow
from api.serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer
)
from rest_framework import filters
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from api.permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с постами.

    Предоставляет стандартные действия: list, retrieve, create, update,
    partial_update, destroy.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Создает новый пост.

        Args:
            serializer (PostSerializer): Сериализатор для создания поста.

        При создании поста автоматически устанавливает текущего пользователя
        как автора.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.

    Предоставляет стандартные действия: list, retrieve, create, update,
    partial_update, destroy.
    Комментарии фильтруются по post_id, указанному в URL.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_post(self):
        """Метод для получения поста или ошибки 404."""
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        """
        Возвращает комментарии, отфильтрованные по post_id.

        Returns:
            QuerySet: Список комментариев, связанных с указанным постом.
        """
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """
        Создает новый комментарий.

        Args:
            serializer (CommentSerializer):
            Сериализатор для создания комментария.

        При создании комментария автоматически устанавливает текущего
        пользователя как автора и связывает комментарий с постом, указанным в
        URL.
        """
        serializer.save(
            author=self.request.user, post=self.get_post()
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с группами.

    Предоставляет только чтение (list и retrieve) для модели Group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """

    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def validate_following(self, data):
        if data == self.context['request'].user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return data

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
