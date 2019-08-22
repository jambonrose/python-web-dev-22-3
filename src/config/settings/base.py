"""Django settings for Startup Organizer Project

Built during Andrew Pinkham's class on Safari Books Online.

https://docs.djangoproject.com/en/2.2/topics/settings/
https://docs.djangoproject.com/en/2.2/ref/settings/
https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
"""

from environ import Env, Path

from .. import checks  # noqa: F401

ENV = Env()

BASE_DIR = Path(__file__) - 3

SECRET_KEY = ENV.str("SECRET_KEY")

DEBUG = ENV.bool("DEBUG", default=False)

ALLOWED_HOSTS = ENV.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "0.0.0.0", "::1"],
)

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "oauth2_provider",
    "corsheaders",
    "url_checks.apps.UrlChecksConfig",
    # first party
    "blog.apps.BlogConfig",
    "organizer.apps.OrganizerConfig",
    "user.apps.UserConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": ENV.db(
        "DATABASE_URL",
        default=f"sqlite:////{BASE_DIR}/db.sqlite3",
    )
}


def get_memcache_config():
    """Load config from ENV, or assume Heroku deploy

    https://devcenter.heroku.com/articles/memcachier#django
    """
    if ENV.get_value("MEMCACHE_URL", default=None):
        return ENV.cache("MEMCACHE_URL")
    location = ENV.get_value(
        "MEMCACHIER_SERVERS", default=None
    )
    if location:
        return {
            "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
            "TIMEOUT": None,  # default key expiration, NOT connection timeout
            "LOCATION": ENV.str("MEMCACHIER_SERVERS"),
            "OPTIONS": {
                "binary": True,
                "username": ENV.str("MEMCACHIER_USERNAME"),
                "password": ENV.str("MEMCACHIER_PASSWORD"),
                "behaviors": {
                    # Enable faster IO
                    "no_block": True,
                    "tcp_nodelay": True,
                    # Keep connection alive
                    "tcp_keepalive": True,
                    # Timeout settings
                    "connect_timeout": 2000,  # ms
                    "send_timeout": 750 * 1000,  # us
                    "receive_timeout": 750 * 1000,  # us
                    "_poll_timeout": 2000,  # ms
                    # Better failover
                    "ketama": True,
                    "remove_failed": 1,
                    "retry_timeout": 2,
                    "dead_timeout": 30,
                },
            },
        }
    return {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }


CACHE_MIDDLEWARE_KEY_PREFIX = "startuporganizer"
CACHE_MIDDLEWARE_SECONDS = 60

CACHES = {"default": get_memcache_config()}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "user.User"

ACCOUNT_ACTIVATION_DAYS = ENV.int(
    "ACCOUNT_ACTIVATION_DAYS", default=7
)
# https://django-registration.readthedocs.io/en/3.0.1/activation-workflow.html#salt-security
REGISTRATION_SALT = ENV.str(
    "REGISTRATION_SALT", default="registration"
)

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

AUTH_P = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": AUTH_P + "UserAttributeSimilarityValidator",
        "OPTIONS": {
            "user_attributes": (
                "email",
                "full_name",
                "short_name",
            )
        },
    },
    {
        "NAME": AUTH_P + "MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": AUTH_P + "CommonPasswordValidator"},
    {"NAME": AUTH_P + "NumericPasswordValidator"},
]

LOGIN_URL = "auth:login"
LOGIN_REDIRECT_URL = "site_root"
LOGOUT_REDIRECT_URL = "auth:login"

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.IsAuthenticatedOrTokenHasScope",
        "rest_framework.permissions.DjangoModelPermissions",
    ),
}

OAUTH2_PROVIDER = {
    "SCOPES": {
        "newslink": "Access to news article links",
        "post": "Access to blog posts",
        "startup": "Access to startup data",
        "tag": "Access to tag (labels) data",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = BASE_DIR("runtime", "static")
STATIC_URL = "/static/"
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)

##################
# EMAIL SETTINGS #
##################

EMAIL_BACKEND = ENV.str(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

DEFAULT_FROM_EMAIL = ENV.str(
    "DEFAULT_FROM_EMAIL", default=""
)
SERVER_EMAIL = ENV.str("SERVER_EMAIL", default="")

EMAIL_HOST = ENV.str("EMAIL_HOST", default="")
EMAIL_PORT = ENV.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = True

EMAIL_HOST_USER = ENV.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = ENV.str(
    "EMAIL_HOST_PASSWORD", default=""
)

NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--allow-root",
    "--no-browser",
]
