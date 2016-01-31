"""
Django settings for the RSSNext project.
"""

import os

from configurations import Configuration

import rssnext.local_settings as local_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Base(Configuration):
    """
    Settings which shall apply to both dev and production environments.
    """

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

    SECRET_KEY = local_settings.SECRET_KEY

    SERVER_EMAIL = 'noreply@rssnext.net'
    ADMINS = (('Joseph Schilz', 'joseph.schilz@gmail.com'),)

    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'rssnext',
        'subscription',
        'feedreader',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
        # 'sslify',
        'rest_framework',
        'paypal.standard.ipn',

    )

    MIDDLEWARE_CLASSES = (
        # 'sslify.middleware.SSLifyMiddleware', # This goes first
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    PAYPAL_RECEIVER_EMAIL = "joseph.schilz@gmail.com"

    ROOT_URLCONF = 'rssnext.urls'

    WSGI_APPLICATION = 'rssnext.wsgi.application'

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    DEFAULT_FROM_EMAIL = "noreply@rssnext.net"


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/
    STATIC_URL = '/static/'

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",
        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend"
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
    )

    LOGIN_REDIRECT_URL = '/home'

    ACCOUNT_LOGOUT_ON_GET = True
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    SOCIALACCOUNT_QUERY_EMAIL = True
    SOCIALACCOUNT_PROVIDERS = {
        'facebook': {
            'SCOPE': ['email', 'publish_stream'],
            'METHOD': 'js_sdk'  # instead of 'oauth2'
        }
    }

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
        'PAGINATE_BY': 10
    }


    SITE_ID = 1

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    PAYPAL_IMAGE = '/static/rssnext/media/paypal_buy.gif'
    PAYPAL_SANDBOX_IMAGE = PAYPAL_IMAGE

    NON_PREMIUM_MAX_SUBSCRIPTIONS = 30
    PREMIUM_MAX_SUBSCRIPTIONS = 200


class Dev(Base):
    """
    Settings which shall apply only to dev environments.
    """

    DEBUG = True
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    PAYPAL_TEST = True

    NON_PREMIUM_MAX_SUBSCRIPTIONS = 5


class Production(Base):
    """
    Settings which shall apply only to production environments.
    """

    import pymysql
    pymysql.install_as_MySQLdb()

    ALLOWED_HOSTS = ['.rssnext.net']

    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'rssnext_db',
            'USER': 'awsuser',
            'PASSWORD': local_settings.DB_PASSWORD,
            'HOST': 'rssnext-dbinstance.cy0oi4yfufio.us-east-1.rds.amazonaws.com',
            'PORT': '3306',
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True

    PAYPAL_TEST = False
