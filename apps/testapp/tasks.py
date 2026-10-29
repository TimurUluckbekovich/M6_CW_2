import time

from celery import shared_task


@shared_task
def send_welcome_email_task(user_email):
    """
    Имитация отправки приветственного письма.
    Выполняется отдельным Celery Worker.
    """

    print(
        f"Celery Worker: Sending welcome email to {user_email}...",
        flush=True,
    )

    time.sleep(5)

    print(
        f"Celery Worker: Welcome email sent to {user_email}.",
        flush=True,
    )

    return {
        "email": user_email,
        "status": "sent",
    }


@shared_task
def clear_expired_cache_task():
    """
    Периодическая задача Celery Beat.
    """

    print(
        "Beat Task: Cleaning expired items...",
        flush=True,
    )