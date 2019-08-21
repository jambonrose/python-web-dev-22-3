"""Demonstrate & validate OAuth flows"""
import base64
import json
from urllib.parse import parse_qs, urlparse

from test_plus.test import TestCase

from improved_user.factories import UserFactory
from oauth2_provider.models import get_application_model

OAuth_App = get_application_model()


class TestOAuthRoutes(TestCase):
    """Integration tests to simulate User interaction"""

    user_factory = UserFactory

    def test_oauth_auth_code_grant_workflow(self):
        """Can we authorize via Authorization Code?"""
        basic_user = self.make_user(
            "basic_user@test.com",
            perms=["organizer.view_startup"],
        )
        app = OAuth_App.objects.create(
            user=basic_user,
            name="Auth Code Example App",
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_AUTHORIZATION_CODE,
            redirect_uris="http://thirdparty.com/exchange/",
        )

        # a user is directed to a link, and asked to login
        self.get(
            "oauth2_provider:authorize",
            data={
                "client_id": app.client_id,
                "response_type": "code",
                "state": "random_state_string",
            },
        )
        self.response_302()
        expected_redirect = (
            "{}?next={}"
            "%3Fclient_id%3D{}"
            "%26response_type%3D{}"
            "%26state%3D{}".format(
                self.reverse("auth:login"),
                self.reverse("oauth2_provider:authorize"),
                app.client_id,
                "code",
                "random_state_string",
            )
        )
        self.assertEqual(
            self.last_response.url, expected_redirect
        )

        # we login the user, and then proceed
        with self.login(basic_user):
            # with the login, we ask for the same page as before
            # the site asks whether the user would like to allow
            # the third party site to access data on this provider site
            self.get_check_200(
                "oauth2_provider:authorize",
                data={
                    "client_id": app.client_id,
                    "response_type": "code",
                    "state": "random_state_string",
                },
            )
            # the user, presumably, responds with a yes
            self.post(
                "oauth2_provider:authorize",
                data={
                    # from third party app
                    "client_id": app.client_id,
                    "response_type": "code",
                    "state": "random_state_string",
                    # put in form by Django
                    "redirect_uri": "http://thirdparty.com/exchange/",
                    "scope": "newslink post startup tag",
                    "allow": "Authorize",
                },
            )
            # the Django site will subsequently redirect to the third party
            # providing a code in the process
            self.response_302()
            token_code = parse_qs(
                urlparse(self.last_response.url).query
            )["code"]

        # the third party site should use this code to ask for a token
        self.post(
            "oauth2_provider:token",
            data={
                "client_id": app.client_id,
                "cleint_secret": app.client_secret,
                "code": token_code,
                "redirect_uri": "http://thirdparty.com/exchange/",
                "grant_type": "authorization_code",
            },
        )
        token_data = self.last_response.json()
        self.assertIn("access_token", token_data)
        self.assertIn("refresh_token", token_data)
        self.assertIn("token_type", token_data)
        self.assertIn("expires_in", token_data)

        # this token can be used to access data
        self.get_check_200(
            self.reverse("api-startup-list"),
            extra={
                "HTTP_AUTHORIZATION": "{} {}".format(
                    token_data["token_type"],
                    token_data["access_token"],
                )
            },
        )

    def test_oauth_password_grant_workflow(self):
        """Can we authorize via Password?"""
        basic_user = self.make_user(
            "basic_user@test.com",
            perms=["organizer.view_startup"],
        )
        app = OAuth_App.objects.create(
            user=basic_user,
            name="Password Grant Example App",
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://example.com",
        )

        # a third party site prompts the user for username and password
        # and then sends that data to us
        token_request_data = {
            "grant_type": "password",
            "username": "basic_user@test.com",
            "password": "password",
        }
        user_pass = "{0}:{1}".format(
            app.client_id, app.client_secret
        )
        auth_string = base64.b64encode(
            user_pass.encode("utf-8")
        )
        self.post(
            "oauth2_provider:token",
            data=token_request_data,
            extra={
                "HTTP_AUTHORIZATION": "Basic {}".format(
                    auth_string.decode("utf8")
                )
            },
        )
        self.response_200()

        # the site should return a token
        # the token shoule be used to consume data from the API
        content = json.loads(
            self.last_response.content.decode("utf-8")
        )
        access_token = content["access_token"]
        token_type = content["token_type"]
        self.get_check_200(
            self.reverse("api-startup-list"),
            extra={
                "HTTP_AUTHORIZATION": "{} {}".format(
                    token_type, access_token
                )
            },
        )
