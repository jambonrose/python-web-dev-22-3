"""Views for the Test app"""
from django.http import HttpResponse
from django.views.decorators.http import (
    require_http_methods,
)


@require_http_methods(["GET", "HEAD", "OPTIONS"])
def pong(request):
    """Respond to ping requests"""
    return HttpResponse("pong")
