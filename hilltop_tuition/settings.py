from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

# Load env for local dev
if os.path.exists(BASE_DIR / '.env'):
    from dotenv import load_dotenv
    load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
AZURE_DEPLOYED = (
    os.getenv('AZURE_DEPLOYED',
              os.getenv('azure_deployed', 'false'))
).lower() == 'true'
DEBUG = not AZURE_DEPLOYED
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',') if AZURE_DEPLOYED else ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'home',
]

CSRF_TRUSTED_ORIGINS = [
    "https://mattyswebsite-chcbefabg8c3hsf8.uksouth-01.azurewebsites.net",
    "https://hilltoptuition.com",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hilltop_tuition.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'hilltop_tuition.wsgi.application'

if AZURE_DEPLOYED:
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
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

# Azure Blob storage for static and media
AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY  = os.getenv('AZURE_ACCOUNT_KEY')

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

STATICFILES_STORAGE  = 'hilltop_tuition.settings.StaticStorage'
DEFAULT_FILE_STORAGE = 'hilltop_tuition.settings.MediaStorage'

STATIC_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/static/'
MEDIA_URL  = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/media/'

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT  = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
