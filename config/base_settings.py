import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

"""Load ENV Globally when in dev"""
if os.environ.get("DJANGO_ENV") != "production":
    from dotenv import load_dotenv

    ENV_PATH = Path.joinpath(BASE_DIR, ".env")
    load_dotenv(dotenv_path=ENV_PATH)
    DEBUG = True


SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # third-party
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "corsheaders",
    "durationwidget",
    "drf_spectacular",
    # custom
    "accounts.apps.AccountsConfig",
    "powerbi.apps.PowerbiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "accounts", "templates"),
        ],
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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

"""Localization and Timezone"""
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_L10N = True
USE_TZ = True

"""Static Assets"""
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

"""MSAL Configuration"""
MSAL_CONFIG = {
    "AUTHENTICATION_MODE": os.getenv("AUTHENTICATION_MODE"),
    "WORKSPACE_ID": os.getenv("WORKSPACE_ID"),
    "REPORT_ID": os.getenv("REPORT_ID"),
    "TENANT_ID": os.getenv("TENANT_ID"),
    "CLIENT_ID": os.getenv("CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("CLIENT_SECRET"),
    "SCOPE": ["https://analysis.windows.net/powerbi/api/.default"],
    "AUTHORITY": "https://login.microsoftonline.com/organizations",
    "POWER_BI_USER": os.getenv("POWER_BI_USER"),
    "POWER_BI_PASS": os.getenv("POWER_BI_PASS"),
}

"""CustomUser as default AUTH model"""
AUTH_USER_MODEL = "accounts.CustomUser"

"""Allowed CORS origins"""
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    os.getenv("CLIENT_SITE"),
]
CORS_ALLOW_CREDENTIALS = True

"""DRF Permission and Authentication"""
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.IsAdminUser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

"""dj-rest-auth configuration inherited from allauth"""
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
OLD_PASSWORD_FIELD_ENABLED = True
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

SITE_ID = 1

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "accounts.serializers.UserSerializer",
    "LOGIN_SERIALIZER": "accounts.serializers.LoginSerializer",
}

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "accounts.serializers.RegistrationSerializer",
}

"""SIMPLEJWT Config"""
REST_USE_JWT = True
JWT_AUTH_COOKIE = "atok"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Magpie Data Platform API",
    "LICENSE": {"name": "MIT"},
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@3.35.1",
}
