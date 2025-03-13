from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Поля:
    - id: Уникальный идентификатор поста.
    - text: Текст поста.
    - pub_date: Дата публикации поста.
    - author: Имя автора поста (только для чтения).
    - group: Группа, к которой относится пост.
    - image: Изображение, прикрепленное к посту.
    """

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Поля:
    - id: Уникальный идентификатор комментария.
    - author: Имя автора комментария (только для чтения).
    - text: Текст комментария.
    - created: Дата создания комментария.
    - post: Идентификатор поста, к которому относится комментарий
            (только для чтения).
    """

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.

    Поля:
    - id: Уникальный идентификатор группы.
    - title: Название группы.
    - description: Описание группы.
    - slug: Уникальный идентификатор группы для URL.
    """

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и валидации подписок между пользователями.

    Поля:
    - user (slug): Имя пользователя, который подписывается. Автоматически
      устанавливается как текущий аутентифицированного пользователя.
      Только для чтения.
    - following (slug): Имя пользователя, на которого происходит подписка.
                        Должно существовать в системе.

    Валидация:
    - Запрещена подписка на самого себя
      (проверка в методе 'validate_following').
    - Запрещены дублирующиеся подписки (валидатор UniqueTogetherValidator).
    """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate_following(self, data):
        """
        Проверяет, что пользователь не пытается подписаться на самого себя.

        Аргументы:
            data (User): Объект пользователя, полученный из slug 'username'.
        Исключения:
            ValidationError: Если текущий пользователь совпадает с following.
        Возвращает:
            User: Валидный объект пользователя для подписки.
        """
        if data == self.context['request'].user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return data
