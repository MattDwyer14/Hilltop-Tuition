"""
Django settings for Hilltop Tuition – production-ready for Azure App Service
with static & media files on Azure Blob Storage via Managed Identity.
"""

from pathlib import Path
import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from storages.backends.azure_storage import AzureStorage

# ─── BASE ───────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

# Load .env only for local development
if (BASE_DIR / ".env").exists():
    load_dotenv()

# ─── CORE SETTINGS ─────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY")

AZURE_DEPLOYED = os.getenv("AZURE_DEPLOYED") == "true"
DEBUG = not AZURE_DEPLOYED

if AZURE_DEPLOYED:
    ALLOWED_HOSTS = [
        "hilltoptuition.com",
        "www.hilltoptuition.com",
        # Azure default host:
        "hilltop-tuition-prod.azurewebsites.net",
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
    "https://hilltop-tuition-prod.azurewebsites.net",
    "https://hilltoptuition.com",
]

# ─── DATABASES ─────────────────────────────────────────────────────────────────
if AZURE_DEPLOYED:
    DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql',
        'HOST'    : os.getenv['DB_HOST'],
        'PORT'    : '5432',
        'NAME'    : os.getenv['DB_NAME'],
        'USER'    : os.getenv['DB_USER'],
        'PASSWORD': os.getenv['DB_PASSWORD'],
        'OPTIONS' : {'sslmode': 'require'},
        }
    }
    
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME":   BASE_DIR / "db.sqlite3",
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
    STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    credential = DefaultAzureCredential()

    class StaticStorage(AzureStorage):
        account_name    = STORAGE_ACCOUNT
        credential      = credential
        azure_container = "static"
        expiration_secs = None

    class MediaStorage(AzureStorage):
        account_name    = STORAGE_ACCOUNT
        credential      = credential
        azure_container = "media"
        expiration_secs = None

    STATICFILES_STORAGE  = "hilltop_tuition.settings.StaticStorage"
    DEFAULT_FILE_STORAGE = "hilltop_tuition.settings.MediaStorage"

    STATIC_URL = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/static/"
    MEDIA_URL  = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/media/"
else:
    STATIC_URL = "/static/"
    MEDIA_URL  = "/media/"

# ─── STATIC FILES (local dev only) ────────────────────────────────────────────
if not AZURE_DEPLOYED:
    STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT  = BASE_DIR / "media"
