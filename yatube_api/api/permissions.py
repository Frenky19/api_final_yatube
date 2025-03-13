from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее редактировать объект только автору.

    Логика:
    - Для безопасных методов (GET, HEAD, OPTIONS) доступ разрешён всем.
    - Для методов, изменяющих объект (POST, PUT, PATCH, DELETE), доступ
      разрешён только автору объекта (проверка по полю 'author').

    Пример использования:
    - Разрешение применяется к объектам, у которых есть поле 'author',
      например, посты или комментарии.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь право на выполнение действия.

        Аргументы:
            request (HttpRequest): Запрос от клиента.
            view (APIView): Представление, обрабатывающее запрос.
            obj: Объект, к которому проверяется доступ.
        Возвращает:
            bool: True, если доступ разрешён, иначе False.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
