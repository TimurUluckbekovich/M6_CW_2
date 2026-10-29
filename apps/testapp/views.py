import time

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tasks import send_welcome_email_task


STATS_CACHE_KEY = "api:v1:stats"


@api_view(["GET"])
def stats(request):
    """
    Возвращает статистику.
    Результат хранится в Redis 60 секунд.
    """

    data = cache.get(STATS_CACHE_KEY)

    if data is None:
        print(
            "Stats cache miss: generating statistics...",
            flush=True,
        )

        # Имитация тяжёлого вычисления.
        time.sleep(2)

        data = {
            "users_count": 1000,
            "active_orders": 42,
        }

        cache.set(STATS_CACHE_KEY, data, timeout=60)

    else:
        print("Stats cache hit", flush=True)

    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register(request):
    """
    Принимает email и ставит задачу отправки письма в очередь.
    Не ждёт завершения Celery-задачи.
    """

    email = request.data.get("email")

    if not isinstance(email, str) or not email.strip():
        return Response(
            {"email": "Это поле обязательно."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    email = email.strip()

    try:
        validate_email(email)
    except ValidationError:
        return Response(
            {"email": "Введите корректный email."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Отправляем задачу в очередь, не вызывая её напрямую.
    task = send_welcome_email_task.delay(email)

    return Response(
        {
            "message": "Регистрация принята. Письмо поставлено в очередь.",
            "email": email,
            "task_id": task.id,
        },
        status=status.HTTP_201_CREATED,
    )