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

ALLOWED_HOSTS = []

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
    "url_checks.apps.UrlChecksConfig",
    # first party
    "blog.apps.BlogConfig",
    "organizer.apps.OrganizerConfig",
    "user.apps.UserConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "user.User"

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

# EMail configuration
EMAIL_BACKEND = ENV.str(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--allow-root",
    "--no-browser",
]
