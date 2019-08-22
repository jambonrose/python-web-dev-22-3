"""Development settings for Startup Organizer"""
from .base import *  # noqa: F403

INSTALLED_APPS.append("debug_toolbar")  # noqa: F405

DEBUG = ENV.bool("DEBUG", default=True)  # noqa: F405

MIDDLEWARE.insert(  # noqa: F405
    4, "debug_toolbar.middleware.DebugToolbarMiddleware"
)


def show_toolbar(request):
    """Use env variable to decide when to show debug tooolbar"""
    return ENV.bool(  # noqa: F405
        "SHOW_DEBUG_TOOLBAR", default=DEBUG
    )


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar
}

TEMPLATES[0]["OPTIONS"].update(  # noqa: F405
    {
        "debug": ENV.bool(  # noqa: F405
            "TEMPLATE_DEBUG", default=True
        )
    }
)

# https://github.com/evansd/whitenoise/issues/191
# Normally set to settings.DEBUG, but tests run with DEBUG=FALSE!
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True
