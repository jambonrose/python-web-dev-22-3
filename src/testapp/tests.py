"""Tests that demonstrate how to write tests in Django"""
from django.test import TestCase
from django.urls import reverse


class DemoTests(TestCase):
    """Demonstration of basic testing patterns"""

    def test_ping_get(self):
        """Can we ping the server with GET?"""
        response = self.client.get("/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode("utf8"), "pong"
        )

    def test_ping_head(self):
        """Can we ping the server with HEAD?"""
        response = self.client.head("/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertGreater(
            int(response["Content-Length"]), 0
        )

    def test_ping_options(self):
        """Can we ping the server for OPTIONS?"""
        response = self.client.options("/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertEqual(response["Content-Length"], "0")
        for method in ["GET", "HEAD", "OPTIONS"]:
            with self.subTest(method=method):
                self.assertIn(
                    method,
                    response["Allow"],
                    f"{method} not in ALLOW header",
                )

    def test_ping_method_not_allowed(self):
        """Do we handle disallowed HTTP methods?"""
        not_allowed = [
            "post",
            "put",
            "patch",
            "delete",
            "trace",
        ]
        for method in not_allowed:
            with self.subTest(method=method):
                call_method = getattr(self.client, method)
                response = call_method("/ping/")
                self.assertEqual(response.status_code, 405)

    def test_status_get(self):
        """Test the status page"""
        url = reverse("site_status")
        self.assertEqual(url, "/status/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        templates = [
            "base.html",
            "testapp/base.html",
            "testapp/status.html",
        ]
        for t_name in templates:
            with self.subTest(template=t_name):
                self.assertTemplateUsed(response, t_name)
        self.assertIn("status", response.context)
        self.assertEqual(response.context["status"], "Good")
        # Django provides its own assertions
        # https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.SimpleTestCase.assertInHTML
        self.assertInHTML(
            "<p>Status is Good</p>",
            response.content.decode("utf8"),
        )
