"""Test authentication views"""
from django.contrib.auth import SESSION_KEY
from django.urls import reverse
from test_plus import TestCase

from improved_user.factories import UserFactory


class AuthenticationViewTests(TestCase):
    """Ensure login and logout workon via the browser"""

    user_factory = UserFactory

    @classmethod
    def setUpTestData(cls):
        """Create a user for test usage"""
        cls.password = "securepassword!"
        cls.user = cls.make_user(password=cls.password)

    def test_login_get(self):
        """Can users GET a login form?"""
        login_url = reverse("auth:login")
        blog_url = reverse("post_list")
        params = [
            (login_url, False, None),
            (
                f"{login_url}?next={blog_url}",
                True,
                blog_url,
            ),
        ]
        for get_url, extra_field, redirect_url in params:
            with self.subTest(
                get=get_url,
                with_next_field=extra_field,
                redirect_to=redirect_url,
            ):
                response = self.get_check_200(get_url)
                self.assertInContext("form")
                templates = [
                    "base.html",
                    "user/base.html",
                    "user/login.html",
                ]
                for t_name in templates:
                    with self.subTest(template=t_name):
                        self.assertTemplateUsed(
                            response, t_name
                        )
                next_field = (
                    f"<input"
                    f' type="hidden"'
                    f' name="next"'
                    f' value="{blog_url}"'
                    f">"
                )
                if extra_field:
                    self.assertResponseContains(next_field)
                else:
                    self.assertResponseNotContains(
                        next_field
                    )

    def test_login_post(self):
        """Can users login to the site?"""
        login_url = reverse("auth:login")
        blog_url = reverse("post_list")
        params = [
            (login_url, None, reverse("site_root")),
            (login_url, blog_url, blog_url),
            (
                f"{login_url}?next={blog_url}",
                None,
                blog_url,
            ),
        ]
        for post_url, extra_data, redirect_url in params:
            with self.subTest(
                post=post_url,
                extra=extra_data,
                redirect_to=redirect_url,
            ):
                data = {
                    "username": self.user.email,
                    "password": self.password,
                }
                if extra_data:
                    data["next"] = extra_data
                response = self.post(post_url, data=data)
                self.assertIn(
                    SESSION_KEY, self.client.session
                )
                self.assertRedirects(
                    response,
                    redirect_url,
                    fetch_redirect_response=False,
                )
                self.get_check_200(response.url)
                self.assertInContext("messages")
                name = self.user.get_short_name()
                self.assertIn(
                    f"Successfully logged in as {name}",
                    [
                        str(m)
                        for m in self.context["messages"]
                    ],
                )

    def test_logout_get(self):
        """Can users logout via GET request?"""
        with self.login(self.user, password=self.password):
            response = self.get("auth:logout")
            self.assertNotIn(
                SESSION_KEY, self.client.session
            )
            self.assertRedirects(
                response,
                reverse("auth:login"),
                fetch_redirect_response=False,
            )
            self.get_check_200(response.url)
            self.assertInContext("messages")
            self.assertIn(
                "Successfully logged out",
                [str(m) for m in self.context["messages"]],
            )
