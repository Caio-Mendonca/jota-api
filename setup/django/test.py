from .base import *
import tempfile

# Based on https://www.hacksoft.io/blog/optimize-django-build-to-run-faster-on-github-actions

MEDIA_ROOT = tempfile.gettempdir()
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}