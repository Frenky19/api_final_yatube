from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Модель поста для работы в админке."""

    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Модель группы для работы в админке."""


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Модель комментария для работы в админке."""


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Модель управления подписками для работы в админке."""
