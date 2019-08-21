"""Check internal routes for OAuth apps"""
from test_plus.test import TestCase

from improved_user.factories import UserFactory
from oauth2_provider.models import get_application_model

OAuth_App = get_application_model()


class TestOAuthRoutes(TestCase):
    """Can we access expected routes?"""

    user_factory = UserFactory

    def test_application_display(self):
        """Can we access display (detail/list) pages?"""
        basic_user = self.make_user("basic_user@test.com")
        app_name = "Password Grant Example App"
        app = OAuth_App.objects.create(
            user=basic_user,
            name=app_name,
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://example.com",
        )

        self.assertLoginRequired("oauth2_provider:list")
        self.assertLoginRequired(
            "oauth2_provider:detail", pk=app.pk
        )

        with self.login(basic_user):
            self.get_check_200("oauth2_provider:list")
            self.assertResponseContains(
                app_name, html=False
            )
            self.get_check_200(
                "oauth2_provider:detail", pk=app.pk
            )
            self.assertResponseContains(
                app_name, html=False
            )

    def test_application_creation_workflow(self):
        """Can we create new applications?"""
        basic_user = self.make_user("basic_user@test.com")

        self.assertLoginRequired("oauth2_provider:register")

        with self.login(basic_user):
            self.get_check_200("oauth2_provider:register")
            app_name = "Password Grant Example App"
            form_data = {
                "name": app_name,
                "client_id": "client_id",
                "client_secret": "client_secret",
                "client_type": OAuth_App.CLIENT_PUBLIC,
                "redirect_uris": "http://example.com",
                "authorization_grant_type": OAuth_App.GRANT_PASSWORD,
            }
            self.post(
                "oauth2_provider:register", data=form_data
            )
            self.response_302()
            self.assertTrue(
                OAuth_App.objects.filter(
                    name=app_name
                ).exists()
            )
            self.get_check_200("oauth2_provider:list")
            self.assertResponseContains(
                app_name, html=False
            )
            app_pk = OAuth_App.objects.get(name=app_name).pk
            self.get_check_200(
                "oauth2_provider:detail", pk=app_pk
            )

    def test_application_update_workflow(self):
        """Can we update an existing application?"""
        basic_user = self.make_user("basic_user@test.com")
        app_name = "Password Grant Example App"
        app = OAuth_App.objects.create(
            user=basic_user,
            name="Password Grant Example App",
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://example.com",
        )

        self.assertLoginRequired(
            "oauth2_provider:update", pk=app.pk
        )

        with self.login(basic_user):
            self.get_check_200(
                "oauth2_provider:detail", pk=app.pk
            )
            self.assertResponseContains(
                app_name, html=False
            )
            self.get_check_200(
                "oauth2_provider:update", pk=app.pk
            )
            new_app_name = "New App Name"
            form_data = {
                "user": basic_user.pk,
                "name": new_app_name,
                "client_id": "client_id",
                "client_secret": "client_secret",
                "client_type": OAuth_App.CLIENT_PUBLIC,
                "redirect_uris": "http://example.com",
                "authorization_grant_type": OAuth_App.GRANT_PASSWORD,
            }
            self.post(
                "oauth2_provider:update",
                pk=app.pk,
                data=form_data,
            )
            self.response_302()
            self.assertFalse(
                OAuth_App.objects.filter(
                    name=app_name
                ).exists()
            )
            self.assertTrue(
                OAuth_App.objects.filter(
                    name=new_app_name
                ).exists()
            )
            self.get_check_200(
                "oauth2_provider:detail", pk=app.pk
            )
            self.assertResponseContains(
                new_app_name, html=False
            )
            self.assertResponseNotContains(
                app_name, html=False
            )

    def test_application_deletion(self):
        """Can we remove existing applications?"""
        basic_user = self.make_user("basic_user@test.com")
        app_name = "Password Grant Example App"
        app = OAuth_App.objects.create(
            user=basic_user,
            name=app_name,
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://example.com",
        )

        self.assertLoginRequired(
            "oauth2_provider:delete", pk=app.pk
        )

        with self.login(basic_user):
            self.get_check_200(
                "oauth2_provider:detail", pk=app.pk
            )
            self.assertResponseContains(
                app_name, html=False
            )
            self.get_check_200(
                "oauth2_provider:delete", pk=app.pk
            )
            self.post("oauth2_provider:delete", pk=app.pk)
            self.response_302()
            self.assertFalse(
                OAuth_App.objects.filter(pk=app.pk).exists()
            )
            self.response_404(
                self.get(
                    "oauth2_provider:detail", pk=app.pk
                )
            )
