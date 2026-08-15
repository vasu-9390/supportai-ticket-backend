import os
from pathlib import Path
from datetime import timedelta

import dj_database_url
from dotenv import load_dotenv


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-ai-support-ticket-system-secret-key-2026"
)

DEBUG = os.getenv("DEBUG", "True").lower() in (
    "true",
    "1",
    "t",
)

ALLOWED_HOSTS = ["*"]


# ============================================================
# APPLICATION DEFINITION
# ============================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    "django_filters",

    # Local apps
    "users",
    "customers",
    "agents",
    "tickets",
    "ai_engine",
    "analytics",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")


# ------------------------------------------------------------
# RENDER DATABASE
# ------------------------------------------------------------

if DATABASE_URL:

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }


# ------------------------------------------------------------
# LOCAL DATABASE
# ------------------------------------------------------------

else:

    USE_SQLITE = os.getenv(
        "USE_SQLITE_FALLBACK",
        "False"
    ).lower() in (
        "true",
        "1",
        "t",
    )

    if USE_SQLITE:

        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

    else:

        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",

                "NAME": os.getenv(
                    "DB_NAME",
                    "ai_ticket_db"
                ),

                "USER": os.getenv(
                    "DB_USER",
                    "postgres"
                ),

                "PASSWORD": os.getenv(
                    "DB_PASSWORD",
                    "postgres"
                ),

                "HOST": os.getenv(
                    "DB_HOST",
                    "localhost"
                ),

                "PORT": os.getenv(
                    "DB_PORT",
                    "5432"
                ),
            }
        }


# ============================================================
# CUSTOM USER MODEL
# ============================================================

AUTH_USER_MODEL = "users.User"


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator",

        "OPTIONS": {
            "min_length": 6,
        },
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",

        "rest_framework.authentication.SessionAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    "DEFAULT_RENDERER_CLASSES": (
        "utils.renderers.CustomJSONRenderer",

        "rest_framework.renderers.BrowsableAPIRenderer",
    ),

    "EXCEPTION_HANDLER":
        "utils.exceptions.custom_exception_handler",

    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",

    "PAGE_SIZE": 10,
}


# ============================================================
# SIMPLE JWT
# ============================================================

SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME":
        timedelta(days=7),

    "REFRESH_TOKEN_LIFETIME":
        timedelta(days=30),

    "ROTATE_REFRESH_TOKENS":
        True,

    "BLACKLIST_AFTER_ROTATION":
        False,

    "AUTH_HEADER_TYPES":
        ("Bearer",),
}


# ============================================================
# CORS
# ============================================================

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",

    "http://localhost:5173",

    "http://127.0.0.1:3000",

    "http://127.0.0.1:5173",
]


# ============================================================
# OPENAPI / SWAGGER
# ============================================================

SPECTACULAR_SETTINGS = {

    "TITLE":
        "AI-Powered Ticket Management System API",

    "DESCRIPTION":
        "Enterprise Support SaaS REST APIs "
        "powered by Django & Google Gemini AI",

    "VERSION":
        "1.0.0",

    "SERVE_INCLUDE_SCHEMA":
        False,
}