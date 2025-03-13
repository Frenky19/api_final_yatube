from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

from posts.constants import LIMIT_OF_SYMBOLS


User = get_user_model()


class Group(models.Model):
    """
    Модель для групп.

    Поля:
    - title: заголовок группы;
    - slug: уникальный slug для группы;
    - description: описание группы
    """

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Уникальный слаг')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return Truncator(self.title).chars(LIMIT_OF_SYMBOLS)


class Post(models.Model):
    """
    Модель для постов.

    Поля:
    - text: текст поста;
    - pub_date: дата публикации поста;
    - author: автор поста;
    - image: изображение поста (может быть null);
    - group: группа поста (может быть null)
    """

    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True, verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа'
    )

    class Meta:
        default_related_name = '%(class)ss'

    def __str__(self):
        return Truncator(self.text).chars(LIMIT_OF_SYMBOLS)


class Comment(models.Model):
    """
    Модель для комментариев.

    Поля:
    - author: автор комментария;
    - post: пост, к которому относится комментарий;
    - text: текст комментария;
    - created: дата добавления комментария
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Пост'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата добавления'
    )

    class Meta:
        default_related_name = '%(class)ss'

    def __str__(self):
        sliced_text = Truncator(self.text).chars(LIMIT_OF_SYMBOLS)
        return (
            f'Комментарий автора {self.author} к посту "{self.post}", '
            f'содержание: {sliced_text}'
        )


class Follow(models.Model):
    """
    Модель для хранения подписок пользователя.

    Поля:
    - user (ForeignKey): Пользователь, который подписывается (подписчик).
                        Связан с моделью User через ForeignKey.
    - following (ForeignKey): Пользователь, на которого подписываются.
                            Связан с моделью User через ForeignKey.

    Ограничения:
    - Уникальная пара (user, following) через unique_together,
      чтобы предотвратить дублирование подписок.

    Связанные имена:
    - related_name='follower': Для доступа к подпискам пользователя через
      User.follower.
    - related_name='following': Для доступа к подписчикам пользователя через
      User.following.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан на:'
    )

    class Meta:
        unique_together = ['user', 'following']
