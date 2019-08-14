"""Test authentication views"""
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
