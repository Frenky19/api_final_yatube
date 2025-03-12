from rest_framework import permissions


class IsAuthorOnly(permissions.BasePermission):
    """
    Вспомогательный класс, проверяющий уровень доступа.

    Автору объекта разрешено редактировать или удалять (update,
    partial_update, destroy), остальные могут только читать
    (list и retrieve).
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
