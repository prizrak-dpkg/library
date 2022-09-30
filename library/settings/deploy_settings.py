from .base_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = []


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "****",
        "USER": "****",
        "PASSWORD": "********",
        "HOST": "********",
        "PORT": 3306,
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}


# CKEditor configuration
# https://django-ckeditor.readthedocs.io/en/latest/#optional-customizing-ckeditor-editor

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Media files (Files uploaded by the user)
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-MEDIA_ROOT

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"
