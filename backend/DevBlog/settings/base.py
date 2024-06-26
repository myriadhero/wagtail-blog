"""
Django settings for DevBlog project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from importlib.util import find_spec
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(
        str,
        "django-insecure-w1=ulwq^^v-j^lz!*!oos%!3!aorqr-o0pv*xqbuk2ulbd+s)x",
    ),
    STATICFILES_DIR=(Path, BASE_DIR / "staticfiles"),
    MEDIAFILES_DIR=(Path, BASE_DIR / "media"),
    LOGS_DIR=(Path, BASE_DIR / "logs"),
    DJANGO_ALLOWED_HOSTS=(tuple, ("localhost", "127.0.0.1")),
    DJANGO_URL_PREFIX=(str, None),
    POSTGRES_DB_HOST=(str, "localhost"),
    POSTGRES_DB_PORT=(int, 5432),
    POSTGRES_DB_NAME=(str, "devblogdb"),
    POSTGRES_DB_USER=(str, "postgres"),
    DJANGO_ADMIN_PATH=(str, "admin/"),
    WAGTAIL_ADMIN_PATH=(str, "cms/"),
    WAGTAILADMIN_BASE_URL=(str, "http://example.com"),
    WAGTAIL_SITE_NAME=(str, "DevBlog"),
    DJANGO_TIME_ZONE=(str, "Australia/Sydney"),
)

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")
FORCE_SCRIPT_NAME = env("DJANGO_URL_PREFIX")

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if DEBUG:
    INTERNAL_IPS = [
        "localhost",
        "127.0.0.1",
    ]

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "home",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtailmenus",
    "wagtail_modeladmin",
    "wagtail",
    "wagtailcodeblock",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local custom
    "blog.apps.BlogConfig",
    "weekly_stars.apps.WeeklyStarsConfig",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

if DEBUG and find_spec("debug_toolbar"):
    INSTALLED_APPS.append("debug_toolbar")
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)
    MIDDLEWARE.insert(3, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "DevBlog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
            ],
        },
    },
]

WSGI_APPLICATION = "DevBlog.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # },
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("POSTGRES_DB_HOST"),
        "PORT": env("POSTGRES_DB_PORT"),
        "NAME": env("POSTGRES_DB_NAME"),
        "USER": env("POSTGRES_DB_USER"),
        "PASSWORD": env("POSTGRES_DB_PASSWORD"),
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-au"
TIME_ZONE = env("DJANGO_TIME_ZONE")
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = True
WAGTAIL_APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    if not DEBUG
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)

STATIC_ROOT = env("STATICFILES_DIR")
STATIC_URL = f"{FORCE_SCRIPT_NAME or ''}/static/"

MEDIA_ROOT = env("MEDIAFILES_DIR")
MEDIA_URL = f"{FORCE_SCRIPT_NAME or ''}/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = env("WAGTAIL_SITE_NAME")
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL")
WAGTAIL_ADMIN_PATH = env("WAGTAIL_ADMIN_PATH")
WAGTAIL_CODE_BLOCK_THEME = "okaidia"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    },
}

ADMIN_PATH = env("DJANGO_ADMIN_PATH")
LOGS_DIR = env("LOGS_DIR")
if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOGS_DIR / "django.log",
                "maxBytes": 1024 * 1024 * 5,  # 5MB
                "backupCount": 5,  # 5 total files
                # "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["file"],
            "level": "INFO",
        },
    }
