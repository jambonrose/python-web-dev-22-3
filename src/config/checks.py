"""Checks for suorganizer project

https://docs.djangoproject.com/en/2.2/topics/checks/
"""
from django.apps import apps
from django.core.checks import Tags, Warning, register


@register(Tags.models)
def check_model_str(app_configs=None, **kwargs):
    """Ensure all models define a __str__ method"""
    configs = (
        app_configs
        if app_configs
        else apps.get_app_configs()
    )
    problem_models = [
        model
        for app in configs
        if not app.name.startswith(
            (
                "corsheaders",
                "django.contrib",
                "oauth2_provider",
            )
        )
        for model in app.get_models()
        if "__str__" not in model.__dict__
    ]
    return [
        Warning(
            "All Models must have a __str__ method.",
            hint=(
                "See https://docs.djangoproject.com/"
                "en/2.2/ref/models/instances/#str"
                " for more information."
            ),
            obj=model,
            id="suorganizer.W001",
        )
        for model in problem_models
    ]
