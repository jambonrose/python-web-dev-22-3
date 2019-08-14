"""Test authentication views"""
from re import search as re_search

from django.contrib.auth.views import (
    INTERNAL_RESET_URL_TOKEN,
)
from django.core import mail
from django.urls import reverse
from test_plus import TestCase

from improved_user.factories import UserFactory


class PasswordViewTests(TestCase):
    """Ensure user may modify password via the browser"""

    user_factory = UserFactory

    @classmethod
    def setUpTestData(cls):
        """Store password upon test class instantiation"""
        cls.password = "securepassword!"

    def setUp(self):
        """Create separate user for each test"""
        self.user = self.user_factory(
            password=self.password
        )

    def test_password_change_anonym(self):
        """Is an anonymous user redirected to login?"""
        url = reverse("auth:password_change")
        login_url = reverse("auth:login")
        for method in ["get", "post"]:
            with self.subTest(method=method):
                request = getattr(self, method)
                response = request(url)
                self.assertRedirects(
                    response, f"{login_url}?next={url}"
                )

    def test_password_change_get(self):
        """Is an authenticated user shown a form?"""
        templates = [
            "user/password_change_form.html",
            "user/base.html",
            "base.html",
        ]
        with self.login(self.user, password=self.password):
            r = self.get_check_200("auth:password_change")
            for t_name in templates:
                with self.subTest(template=t_name):
                    self.assertTemplateUsed(r, t_name)

    def test_password_change_post(self):
        """Can an authenticated user change their password?"""
        newpassword = "newsecretpassword!"
        data = {
            "old_password": self.password,
            "new_password1": newpassword,
            "new_password2": newpassword,
        }
        confirm_url = reverse("auth:account")
        with self.login(self.user, password=self.password):
            r = self.post(
                "auth:password_change",
                data=data,
                follow=True,
            )
            self.assertRedirects(r, confirm_url)
            self.user.refresh_from_db()
            self.assertTrue(
                self.user.check_password(newpassword),
                "User's password did not change",
            )
            self.assertInContext("messages")
            self.assertIn(
                "Password Changed Successfully",
                [str(m) for m in self.context["messages"]],
            )

    def test_password_reset_get(self):
        """May anonymous users access password reset?"""
        response = self.get_check_200("auth:password_reset")
        templates = [
            "base.html",
            "user/base.html",
            "user/password_reset_form.html",
        ]
        for t_name in templates:
            with self.subTest(template=t_name):
                self.assertTemplateUsed(response, t_name)

    def test_password_reset(self):
        """Can an anonymous user issue a password reset?"""
        email = self.user.email
        post_response = self.post(
            "auth:password_reset", data={"email": email}
        )
        self.assertRedirects(
            post_response, reverse("auth:login")
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertEqual(
            mail.outbox[0].subject,
            "Password reset on testserver",
        )
        urlmatch = re_search(
            r"https?://[^/]*(/.*reset/\S*)",
            mail.outbox[0].body,
        )
        self.assertIsNotNone(
            urlmatch, "No URL found in sent email"
        )

        url_path = urlmatch.groups()[0]
        *_, uidb64, token = filter(
            None, url_path.split("/")
        )
        self.assertEqual(
            reverse(
                "auth:password_reset_confirm",
                kwargs={"uidb64": uidb64, "token": token},
            ),
            url_path,
        )
        reset_get_response = self.get(url_path)
        # starting in Django 1.11,
        # Django redirects to different token to avoid
        # leaking secret to third-parties included in HTML
        # https://docs.djangoproject.com/en/stable/releases/1.11/#django-contrib-auth
        self.assertRedirects(
            reset_get_response,
            reverse(
                "auth:password_reset_confirm",
                kwargs={
                    "uidb64": uidb64,
                    "token": INTERNAL_RESET_URL_TOKEN,
                },
            ),
        )
        # code below explicitly checks for link
        # but! asserRedirects checks this by default
        # making this test redundant!
        url_path = reset_get_response.url
        reset_get_response = self.get_check_200(url_path)
