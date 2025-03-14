from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer
)
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с постами.

    Предоставляет стандартные действия: list, retrieve, create, update,
    partial_update, destroy.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

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


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для управления подписками пользователя.

    Предоставляет следующие действия:
    - 'list' — получение списка своих подписок (GET /api/v1/follow/).
    - 'create' — подписка на другого пользователя (POST /api/v1/follow/).

    Особенности:
    - Требует аутентификации пользователя.
    - Автоматически привязывает подписку к текущему пользователю при создании.
    - Запрещает подписку на самого себя (возвращает 400 Bad Request).
    - Поиск по username пользователя через параметр 'search':
      /api/v1/follow/?search=username.

    Фильтрация:
    - Поиск по полю 'following__username' через SearchFilter.
    """

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """Возвращает только подписки текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Автоматически назначает текущего пользователя как подписчика."""
        serializer.save(user=self.request.user)
