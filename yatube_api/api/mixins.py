from rest_framework.pagination import LimitOffsetPagination


class PaginationMixin:
    """
    Миксин для динамического включения пагинации в зависимости от параметров.

    Логика:
    - Если в запросе присутствуют параметры 'limit' или 'offset',
      автоматически включается пагинация через 'LimitOffsetPagination'.
    - Если параметры отсутствуют, пагинация отключается, и возвращается полный
      список.

    Пример использования:
    - Применяется в ViewSet для управления пагинацией на уровне запроса.
    - Позволяет клиенту выбирать, нужна ли пагинация, через параметры запроса.

    Примечание:
    - Требует, чтобы ViewSet, использующий миксин, поддерживал
      'pagination_class'.
    """

    def list(self, request, *args, **kwargs):
        """
        Переопределяет метод 'list' для динамического управления пагинацией.

        Аргументы:
            - request (HttpRequest): Запрос от клиента.
            - *args: Дополнительные позиционные аргументы.
            - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            - Response: Ответ с данными, с включенной пагинации или без,
              в зависимости от запроса.
        """
        if 'limit' in request.query_params or 'offset' in request.query_params:
            self.pagination_class = LimitOffsetPagination
        return super().list(request, *args, **kwargs)
