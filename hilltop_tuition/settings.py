"""
Django settings for Hilltop Tuition – production-ready for Azure App Service
with static & media files on Azure Blob Storage via Managed Identity.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from storages.backends.azure_storage import AzureStorage

# ─── BASE ───────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

# Load .env only for local development
if (BASE_DIR / ".env").exists():
    load_dotenv()

# ─── CORE SETTINGS ─────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY")

AZURE_DEPLOYED = os.getenv("AZURE_DEPLOYED") == "true"
DEBUG = True #not AZURE_DEPLOYED

if AZURE_DEPLOYED:
    ALLOWED_HOSTS = [
        "hilltoptuition.com",
        "www.hilltoptuition.com",
        # Azure default host:
        "wa-hilltop-tuition-27042025-d9f9d6azbabxbdd5.uksouth-01.azurewebsites.net",
    ]
else:
    ALLOWED_HOSTS = ["*"]

# ─── APPS & MIDDLEWARE ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "storages",
    # Local
    "home",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hilltop_tuition.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "hilltop_tuition.wsgi.application"

CSRF_TRUSTED_ORIGINS = [
    "https://wa-hilltop-tuition-27042025-d9f9d6azbabxbdd5.uksouth-01.azurewebsites.net",
    "https://hilltoptuition.com",
]

# ─── DATABASES ─────────────────────────────────────────────────────────────────
if AZURE_DEPLOYED:
    DB_NAME     = os.getenv("DB_NAME")
    DB_USER     = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST     = os.getenv("DB_HOST")
    DB_PORT     = os.getenv("DB_PORT")

    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     DB_NAME,
            'USER':     DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST':     DB_HOST,
            'PORT':     DB_PORT
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─── AUTH / I18N / TIME ────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── EMAIL ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND       = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST          = os.getenv("EMAIL_HOST")
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER

# ─── AZURE STORAGE (static & media) ────────────────────────────────────────────
if AZURE_DEPLOYED:
    AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
    AZURE_ACCOUNT_KEY  = os.getenv("AZURE_ACCOUNT_KEY")
    AZURE_STATIC_CONTAINER = os.getenv("AZURE_STATIC_CONTAINER", "static")
    AZURE_MEDIA_CONTAINER  = os.getenv("AZURE_MEDIA_CONTAINER",  "media")

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "account_name": AZURE_ACCOUNT_NAME,
                "account_key": AZURE_ACCOUNT_KEY,
                "azure_container": AZURE_MEDIA_CONTAINER,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "account_name": AZURE_ACCOUNT_NAME,
                "account_key": AZURE_ACCOUNT_KEY,
                "azure_container": AZURE_STATIC_CONTAINER,
            },
        },
    }

    STATIC_URL = (
        f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/"
        f"{AZURE_STATIC_CONTAINER}/"
    )
    MEDIA_URL = (
        f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/"
        f"{AZURE_MEDIA_CONTAINER}/"
    )

    STATIC_URL = f"https://{os.getenv('AZURE_ACCOUNT_NAME')}.blob.core.windows.net/{os.getenv('AZURE_STATIC_CONTAINER', 'static')}/"
    MEDIA_URL = f"https://{os.getenv('AZURE_ACCOUNT_NAME')}.blob.core.windows.net/{os.getenv('AZURE_MEDIA_CONTAINER', 'media')}/"

else:
    STATIC_URL = "/static/"
    MEDIA_URL  = "/media/"

# ─── STATIC FILES (local dev only) ────────────────────────────────────────────
if not AZURE_DEPLOYED:
    STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT  = BASE_DIR / "media"
