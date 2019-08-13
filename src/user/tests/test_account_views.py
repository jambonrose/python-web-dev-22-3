"""Test account views"""
from django.urls import reverse
from test_plus import TestCase

from improved_user.factories import UserFactory


class AccountViewTests(TestCase):
    """Ensure user has account"""

    user_factory = UserFactory

    @classmethod
    def setUpTestData(cls):
        """Store password upon test class instantiation"""
        cls.password = "securepassword!"

    def setUp(self):
        """Create separate user for each test"""
        self.user = self.make_user(password=self.password)

    def test_account_anonym(self):
        """Is an anonymous user redirected to login?"""
        url = reverse("auth:account")
        login_url = reverse("auth:login")
        response = self.get(url)
        self.assertRedirects(
            response, f"{login_url}?next={url}"
        )

    def test_account_display(self):
        """Do authenticated users see a page?"""
        with self.login(self.user, password=self.password):
            response = self.get_check_200("auth:account")
        templates = [
            "base.html",
            "user/base.html",
            "user/account.html",
        ]
        for t_name in templates:
            with self.subTest(template=t_name):
                self.assertTemplateUsed(response, t_name)
        change_pw_url = reverse("auth:password_change")
        self.assertResponseContains(
            f'<a href="{change_pw_url}">', html=False
        )
