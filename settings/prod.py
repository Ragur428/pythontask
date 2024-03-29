"""
Django settings for AJRSv2 project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import datetime
import dj_database_url
import django_heroku

from pathlib import Path
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

print(f"base dir path {BASE_DIR}")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g^o*#kv*twv^)@vam(6=18)rs=pkt2&pevz-1fjza%+o&^nfr!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

print(f"Debug {DEBUG}")

ALLOWED_HOSTS = ['ajrsv2.herokuapp.com', '127.0.0.1:8000']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # 3rd Party Apps
    'mathfilters',
    'ckeditor',
    'rest_framework',
    'django_user_agents',
    'django_celery_beat',
    'rosetta',
    'storages',
    # 'tracking_analyzer',
    # 'haystack',

    # Project Apps
    'shop',
    'account',
    'pages',
    'blog',
    'api',
    'office',
    'bo',
]

MIDDLEWARE = [
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'AJRSv2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates'), ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.context_processors.header_context',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'AJRSv2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


USE_S3 = os.environ.get('USE_S3')

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_URL = os.environ.get('AWS_URL')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'd1thqcs4jslbbb.cloudfront.net'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = AWS_URL + '/static/'
    MEDIA_URL = AWS_URL + '/media/'
    print(f"STatic url {STATIC_URL}")
    STATICFILES_STORAGE = 'AJRSv2.storage_backends.StaticStorage'
    STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)
    DEFAULT_FILE_STORAGE = 'AJRSv2.storage_backends.PublicMediaStorage'
    django_heroku.settings(locals(), staticfiles=False)
else:
    print('else executed')
    STATIC_URL = '/static/'
    MEDIA_URL = 'media/'
    STATICFILES_DIRS = [
        PROJECT_DIR / 'static'
    ]
    STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')
    django_heroku.settings(locals())
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

LOGIN_REDIRECT_URL = '/dash/'

# CELERY CONFIG

CELERY_BROKER_URL = 'redis://:pc92b94424144b00cfcc1e5c362cba84b83d9af79c759356e22ad2b305225a78a@ec2-34-201-239-8' \
                    '.compute-1.amazonaws.com:9460 '
CELERY_RESULT_BACKEND = 'redis://:pc92b94424144b00cfcc1e5c362cba84b83d9af79c759356e22ad2b305225a78a@ec2-34-201-239-8' \
                        '.compute-1.amazonaws.com:9460 '
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# LOCALS SETTINGS
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')),
    ('es', _('Spanish')),
)
LOCALE_PATHS = [
    os.path.join(PROJECT_DIR, 'locale/'),
]

# EMAIL API Settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = "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"

SENDGRID_API_KEY = "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"

# Session Settings
SESSION_ENGINE = "AJRSv2.session_backend"
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# REDIS CACHE CONFIG
#

# CACHES = {
#   'default': {
#       'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#       'LOCATION': 'redis://:pc92b94424144b00cfcc1e5c362cba84b83d9af79c759356e22ad2b305225a78a@ec2-34-201-239-8.compute-1.amazonaws.com:9460',
#    }
# }

# 3rd Party App Settings

STRIPE_PUBLISHABLE_KEY = 'pk_test_Yo5z8x71CRgCD9SsYFsncraJ'
STRIPE_SECRET_KEY = 'sk_test_ekX7BCVgUaA2G2oyuZ20DPjN'
STRIPE_ENDPOINT_SECRET = 'whsec_ohkrMaMTHLFZSRT1ck48Jmbp2aXJguSQ'

AUTHORIZENET_LOGIN_ID = '82gBS2fsX'
AUTHORIZENET_TRANSACTION_KEY = '9a2T794W9JaC9ZpY'

TWILIO_ACCOUNT_SID = 'ACe97afe755470b251698b3fec97107c45'
TWILIO_AUTH_TOKEN = '08312e89f1eddefad1994f85bebd9172'
TWILIO_NUMBER = '+13132024242'

SUMSUB_SECRET_KEY = "CWb2wB8ZLXQARRN2BJpuZueOhDIl9aOk"  # Example: Hej2ch71kG2kTd1iIUDZFNsO5C1lh5Gq
SUMSUB_APP_TOKEN = "sbx:nWJXTSrGRUEiVJR28JNFOTaI.6xkfzov74VOUQFvQwqkQJQirk955uMYg"  # Example: sbx:uY0CgwELmgUAEyl4hNWxLngb.0WSeQeiYny4WEqmAALEAiK2qTC96fBad
SUMSUB_TEST_BASE_URL = "https://api.sumsub.com"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_IMAGE_BACKEND = 'pillow'

AVATAX_USERNAME = 'cyrus@netsoftmlm.com'
AVATAX_PASSWORD = '!PhQ!53TqrWLvD@'
AVATAX_ACCOUNT_ID = '2000303024'
AVATAX_LICENSE_KEY = "D6F6FE3A60D9EBE8"

ESSENTIAL_HUB_API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2NDM0MDUxNzMsImRhdGEiOnsidXNlciI6eyJpZCI6NjA2MywiY3VzdG9tZXJfaWQiOjUxODQsImVtYWlsIjoibmV0cXViZW1hcmtldHBsYWNlZGV2dGVzdEBlc3NlbnRpYWxodWIuY29tIn0sInNjb3BlcyI6WyJhcGlfcHVibGljIl19fQ.IiUnEdDtjzPhAXHFc2quvh1_kFkrn2CLBlawRqiuVdxc4npnsNcriv0QeJtqJ4q2cFkeLzZe0CoozYYijrtDKA'

PAYPAL_CLIENT_ID = 'Aag8K6D2j7Kz4uFHjOVRa4SNCT2dRZZ1sB3PLxAShmjxgg5t48jLWYHWlbV0J-v0OS8nlnQh_Wt9IedZ'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
