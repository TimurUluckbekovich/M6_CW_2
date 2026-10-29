import os

from core.settings.base import *


DEBUG = True

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-local-development-key",
)

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True


# Если задан DB_HOST, используем PostgreSQL.
# Если DB_HOST отсутствует, используем SQLite.
if os.getenv("DB_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "cw2_db"),
            "USER": os.getenv("POSTGRES_USER", "cw2_user"),
            "PASSWORD": os.getenv(
                "POSTGRES_PASSWORD",
                "cw2_password",
            ),
            "HOST": os.getenv("DB_HOST", "db"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }