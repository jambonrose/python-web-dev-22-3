"""Views for the Test app"""
from django.http import HttpResponse
from django.views import View


class Pong(View):
    """Respond to ping requests"""

    def get(self, request):
        """Respond to GET Request"""
        return HttpResponse("pong")
