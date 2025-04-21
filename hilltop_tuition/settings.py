import os
from pathlib import Path

from dotenv import load_dotenv

# ─── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Load .env for local development ────────────────────────────────────────────

load_dotenv(BASE_DIR / '.env')

# ─── Core settings ──────────────────────────────────────────────────────────────

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('AZURE_DEPLOYED', 'false').lower() != 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# ─── Installed apps & middleware ────────────────────────────────────────────────

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third‑party
    'storages',

    # Local
    'home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',            # static fallback
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hilltop_tuition.urls'
WSGI_APPLICATION = 'hilltop_tuition.wsgi.application'

# ─── Templates ─────────────────────────────────────────────────────────────────

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# ─── Database ──────────────────────────────────────────────────────────────────

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }

# ─── Password validation ───────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalisation ───────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ─── Email ─────────────────────────────────────────────────────────────────────

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST       = os.getenv('EMAIL_HOST')
EMAIL_PORT       = 587
EMAIL_USE_TLS    = True
EMAIL_HOST_USER  = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER

# ─── Static & Media ────────────────────────────────────────────────────────────

# Local development:
STATIC_URL = '/static/'
MEDIA_URL  = '/media/'

STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_ROOT       = BASE_DIR / 'media'
STATIC_ROOT      = BASE_DIR / 'staticfiles'

# Use Azure only when deployed
if not DEBUG:
    AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY  = os.getenv('AZURE_ACCOUNT_KEY')

    STATICFILES_STORAGE  = 'hilltop_tuition.settings.StaticStorage'
    DEFAULT_FILE_STORAGE = 'hilltop_tuition.settings.MediaStorage'

    STATIC_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/static/'
    MEDIA_URL  = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/media/'

    from storages.backends.azure_storage import AzureStorage

    class StaticStorage(AzureStorage):
        account_name    = AZURE_ACCOUNT_NAME
        account_key     = AZURE_ACCOUNT_KEY
        azure_container = 'static'
        expiration_secs = None

    class MediaStorage(AzureStorage):
        account_name    = AZURE_ACCOUNT_NAME
        account_key     = AZURE_ACCOUNT_KEY
        azure_container = 'media'
        expiration_secs = None

# ─── Defaults ──────────────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── CSRF trusted hosts (only needed if you have custom domains) ───────────────

CSRF_TRUSTED_ORIGINS = [
    'https://mattyswebsite-chcbefabg8c3hsf8.uksouth-01.azurewebsites.net',
    'https://hilltoptuition.com',
]
