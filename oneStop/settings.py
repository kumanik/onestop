import os
from decouple import config
import dj_database_url
from mongoengine import connect


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config("SECRET_KEY")

DEBUG = config('DEBUG_VAR', default=False, cast=bool)

ALLOWED_HOSTS = [
    "one-1-stop.herokuapp.com",
    "127.0.0.1",
    "localhost",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'widget_tweaks',
    "base",
    "accounts",
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
    'base.middleware.StaffRequiredMiddleware',
]

ROOT_URLCONF = "oneStop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "accounts/templates"),
    os.path.join(BASE_DIR, "base/templates"),
)


WSGI_APPLICATION = "oneStop.wsgi.application"


DATABASES = {
    "default": dj_database_url.config(default=config("DATABASE_URL"))
}

MONGO_HOST = config("MONGO_HOST")
MONGO_NAME = config("MONGO_NAME")

connect(MONGO_NAME, host=MONGO_HOST, alias="default")


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_REDIRECT_URL = '/accounts/check_staff'
LOGOUT_REDIRECT_URL = '/accounts/login'

LOGIN_URL = '/accounts/login/'
REGISTER_URL = '/accounts/register/'

LOGIN_EXEMPT_URLS = (
    '/accounts/login/',
    '/accounts/logout/',
    '/accounts/register/',
    '/accounts/check_staff/',
)
