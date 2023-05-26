"""
Django settings for AJRSv2 project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'django-insecure-g^o*#kv*twv^)@vam(6=18)rs=pkt2&pevz-1fjza%+o&^nfr!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

print(f"{os.environ.get('SECRET_KEY')}")
print(f"project dir {PROJECT_DIR}")
print(f"base dir {BASE_DIR}")
ALLOWED_HOSTS = ['127.0.0.1']

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
    'debug_toolbar',

    # Project Apps

    'shop.apps.ShopConfig',
    'account.apps.AccountConfig',
    'pages.apps.PagesConfig',
    'blog.apps.BlogConfig',
    'api.apps.ApiConfig',
    'office.apps.OfficeConfig',
    'bo.apps.BoConfig',
    'reports.apps.ReportsConfig',
]

MIDDLEWARE = [
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'AJRSv2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR / 'templates']
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

# if DEBUG:
#     STATICFILES_DIRS = [
#         BASE_DIR / 'static'
#     ]
# else:
#     STATIC_ROOT = BASE_DIR / 'staticfiles'


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    PROJECT_DIR / 'static'
]

MEDIA_URL = 'media/'

MEDIA_ROOT = PROJECT_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

LOGIN_REDIRECT_URL = '/dash/'

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'haystack',
#     },
# }

# AUTHENTICATION_BACKENDS = [
#     'api.backends.UrlTokenBackend',
#     'django.contrib.auth.backends.ModelBackend'
#
# ]

STRIPE_PUBLISHABLE_KEY = 'pk_test_Yo5z8x71CRgCD9SsYFsncraJ'
STRIPE_SECRET_KEY = 'sk_test_ekX7BCVgUaA2G2oyuZ20DPjN'
STRIPE_ENDPOINT_SECRET = 'whsec_ohkrMaMTHLFZSRT1ck48Jmbp2aXJguSQ'

AUTHORIZENET_LOGIN_ID = '82gBS2fsX'
AUTHORIZENET_TRANSACTION_KEY = '52jGj86CS4pYx54K'

TWILIO_ACCOUNT_SID = 'ACe97afe755470b251698b3fec97107c45'
TWILIO_AUTH_TOKEN = '08312e89f1eddefad1994f85bebd9172'

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

PAYPAL_PAYOUT_CLIENT_ID = "ARV_wIYrspUazXsf6I-RTBq6eNnVXgOFtHLbH9sATb4_VOL5_d1L0aiQ2JtBwKNoieKORh4bNKqQrD3_"
PAYPAL_PAYOUT_CLIENT_SECRET = "EOred2Z-fM8jG02pn48JCcrN5Rpqe8PcSUpbxhLHk2GB2VcEoGpZzOnybI7hkYW6tbMscsEnk6JcZM6i"

COIN_PAYMENT_API_KEY = 'f4fa2125d90876fc38758b7650a33533f4eb8b1b5ef73a4aec5fa535c85c4613'
COIN_PAYMENT_API_SECRET = '23e30f8f19467B9Daf030e07F7A6299038B87600Ce827eFD2928dd133607e77c'
COIN_PAYMENT_IPN_URL = 'R7`CT58V}P4wE#fW*ed"rw~ZysJa?2,vN='
COIN_PAYMENT_MERCHANT_ID = '1aee87d53be2aab32c0d347faff64cf4'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = [
    PROJECT_DIR / 'locale/'
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = "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"

SENDGRID_API_KEY = "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"

A37_TOKEN = '98c4bf91debe3e043ebcb237c562b20cfeb47e74'

SESSION_ENGINE = "AJRSv2.session_backend"

SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379',
#     }
# }

INTERNAL_IPS = [
    "127.0.0.1",
]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

}

EMAIL_IMAGE_URL = 'http://127.0.0.1:8000/'
DOMAIN_NAME = 'http://127.0.0.1:8000/'