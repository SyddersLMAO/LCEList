from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', default='localhost').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')
GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'markdownify.apps.MarkdownifyConfig',
    'rest_framework',
    'django_filters',
    'drf_spectacular',

    #custom
    'taggit',
    'storages',
    'content',
    'users',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'lcelist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'content.context_processors.site_messages',
                'lcelist.context_processors.analytics',
            ],
        },
    },
]

WSGI_APPLICATION = 'lcelist.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', default='localhost'),
        'PORT': os.environ.get('DB_PORT', default='5432'),
    }
}

# Storage
USE_R2 = os.environ.get('USE_R2', 'False') == 'True'

if USE_R2:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    AWS_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('R2_CUSTOM_DOMAIN', default=None)
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = False

    MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/'
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Allowed markownify tags
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'em',
            'i', 'li', 'ol', 'p', 'strong', 'ul', 'h1', 'h2',
            'h3', 'h4', 'h5', 'h6', 'code', 'pre', 'hr', 'br',
            'img'
        ],
        "WHITELIST_ATTRS": [
            'src', 'alt', 'title', 'width', 'height',
        ],
        "WHITELIST_PROTOCOLS": [
            'http', 'https',
        ],
    }
}

# Rest settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Auth
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'content:index'
LOGOUT_REDIRECT_URL = 'content:index'

# Max file sizes
DATA_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'