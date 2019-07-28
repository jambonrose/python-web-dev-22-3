"""Views for the Test app"""
from django.http import HttpResponse


def pong(request):
    """Respond to ping requests"""
    return HttpResponse("pong")
