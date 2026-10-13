import json
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.test import Client, TestCase
from django.utils import timezone

from integration.models import RegulationDraft, RegulatoryPublication
from personal.models import Harvest, SavedSearch, UserLicense, UserPreference
from regulations.models import LandType, Species

User = get_user_model()
PASSWORD = "Old-Account-QA-passphrase-782!"
NEW_PASSWORD = "New-Account-QA-passphrase-987!"


class AccountManagementTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="hunter", password=PASSWORD)
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.user)

    def change(self, **changes):
        self.client.get("/api/auth/csrf/")
        data = {"current_password": PASSWORD, "new_password": NEW_PASSWORD, "new_password_confirm": NEW_PASSWORD}
        data.update(changes)
        return self.client.post("/api/auth/password/change/", json.dumps(data), content_type="application/json",
                                HTTP_X_CSRFTOKEN=self.client.cookies["csrftoken"].value)

    def test_password_change_keeps_this_session_and_revokes_other_sessions(self):
        other_browser = Client()
        other_browser.force_login(self.user)
        self.assertEqual(self.change().status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(NEW_PASSWORD))
        self.assertFalse(self.user.check_password(PASSWORD))
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 200)
        self.assertEqual(other_browser.get("/api/auth/me/").status_code, 401)

    def test_password_change_validates_current_confirmation_strength_and_csrf(self):
        for changes in [{"current_password": "wrong"}, {"new_password_confirm": "wrong"},
                        {"new_password": "password", "new_password_confirm": "password"},
                        {"new_password": PASSWORD, "new_password_confirm": PASSWORD}]:
            self.assertEqual(self.change(**changes).status_code, 400)
            self.user.refresh_from_db()
            self.assertTrue(self.user.check_password(PASSWORD))
        self.assertEqual(self.client.post("/api/auth/password/change/", {}).status_code, 403)
        self.client.logout()
        self.assertEqual(self.change().status_code, 403)

    def test_suspension_blocks_existing_session_and_admin_password_reset_revokes_sessions(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)
        self.user.is_active = True
        self.user.save(update_fields=["is_active"])
        self.client.force_login(self.user)
        administrator = User.objects.create_superuser(username="qa_admin", password=PASSWORD)
        admin_client = Client()
        admin_client.force_login(administrator)
        response = admin_client.post(f"/admin/auth/user/{self.user.pk}/password/", {
            "password1": NEW_PASSWORD, "password2": NEW_PASSWORD,
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(NEW_PASSWORD))
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)

    def test_support_staff_cannot_reset_administrator_password_or_promote_accounts(self):
        administrator = User.objects.create_superuser(username="qa_admin", password=PASSWORD)
        support = User.objects.create_user(username="qa_support", password=PASSWORD, is_staff=True)
        support.user_permissions.add(*Permission.objects.filter(codename__in=["change_user", "view_user", "delete_user"]))
        self.client.force_login(support)
        self.assertEqual(self.client.get(f"/admin/auth/user/{administrator.pk}/password/").status_code, 403)
        response = self.client.get(f"/admin/auth/user/{self.user.pk}/change/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="is_superuser"')
        self.assertNotContains(response, 'name="is_staff"')
        self.assertEqual(self.client.get("/admin/auth/user/add/").status_code, 403)

    def test_password_change_is_private_marks_all_inputs_sensitive_and_cannot_target_another_account(self):
        other = User.objects.create_user(username="other_hunter", password=PASSWORD)
        response = self.change(user=other.pk, user_id=other.pk, is_staff=True, is_superuser=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.sensitive_post_parameters, "__ALL__")
        self.assertEqual(response["Cache-Control"], "private, no-store")
        self.user.refresh_from_db()
        other.refresh_from_db()
        self.assertTrue(self.user.check_password(NEW_PASSWORD))
        self.assertTrue(other.check_password(PASSWORD))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        for secret in [PASSWORD, NEW_PASSWORD, self.user.password]:
            self.assertNotIn(secret, response.content.decode())

    def test_unsupported_media_and_malformed_password_json_return_private_errors_without_input_echo(self):
        self.client.get("/api/auth/csrf/")
        headers = {"HTTP_X_CSRFTOKEN": self.client.cookies["csrftoken"].value}
        for content_type, body, expected in [
            ("text/plain", f"current_password={PASSWORD}", 415),
            ("application/json", '{"current_password": "' + PASSWORD + '",', 400),
            ("application/json", "null", 400),
            ("application/json", '"' + PASSWORD + '"', 400),
        ]:
            for path in ["/api/auth/password/change/", "/api/personal/licenses/"]:
                with self.subTest(path=path, content_type=content_type, body=body):
                    response = self.client.post(path, body, content_type=content_type, **headers)
                    self.assertEqual(response.status_code, expected, response.content)
                    self.assertEqual(response["Cache-Control"], "private, no-store")
                    self.assertNotIn(PASSWORD, response.content.decode())
                    self.assertNotIn("Traceback", response.content.decode())
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))


class AdminAccountBoundaryTests(TestCase):
    def setUp(self):
        self.hunter = User.objects.create_user(username="managed_hunter", password=PASSWORD)
        self.administrator = User.objects.create_superuser(username="account_admin", password=PASSWORD)
        self.support = User.objects.create_user(username="account_support", password=PASSWORD, is_staff=True)
        self.support.user_permissions.add(*Permission.objects.filter(content_type__app_label="auth", content_type__model="user", codename__in=["view_user", "change_user", "delete_user"]))
        self.client = Client(enforce_csrf_checks=True)

    def admin_post(self, user, path, data, *, csrf=True):
        self.client.force_login(user)
        headers = {}
        if csrf:
            self.client.get("/admin/")
            headers["HTTP_X_CSRFTOKEN"] = self.client.cookies["csrftoken"].value
        return self.client.post(path, data, **headers)

    def user_change_data(self, **extra):
        joined = timezone.localtime(self.hunter.date_joined)
        data = {"username": self.hunter.username, "first_name": "", "last_name": "", "email": "",
                "date_joined_0": joined.strftime("%Y-%m-%d"), "date_joined_1": joined.strftime("%H:%M:%S")}
        data.update(extra)
        return data

    def test_actual_admin_suspension_revokes_hunter_access_without_granting_support_privileges(self):
        hunter_browser = Client()
        hunter_browser.force_login(self.hunter)
        privilege = Permission.objects.get(content_type__app_label="integration", codename="publish_regulationdraft")
        response = self.admin_post(self.support, f"/admin/auth/user/{self.hunter.pk}/change/", self.user_change_data(
            is_staff="on", is_superuser="on", user_permissions=[privilege.pk], _save="Save",
        ))
        self.assertEqual(response.status_code, 302, response.content)
        self.hunter.refresh_from_db()
        self.assertFalse(self.hunter.is_active)
        self.assertFalse(self.hunter.is_staff)
        self.assertFalse(self.hunter.is_superuser)
        self.assertFalse(self.hunter.user_permissions.exists())
        self.assertEqual(hunter_browser.get("/api/auth/me/").status_code, 401)
        self.assertEqual(hunter_browser.get("/api/personal/export/").status_code, 403)

    def test_password_reset_requires_authorized_staff_and_csrf_and_revokes_existing_session(self):
        target_path = f"/admin/auth/user/{self.hunter.pk}/password/"
        data = {"password1": NEW_PASSWORD, "password2": NEW_PASSWORD}
        unprivileged_staff = User.objects.create_user(username="view_only_staff", password=PASSWORD, is_staff=True)
        unprivileged_staff.user_permissions.add(Permission.objects.get(content_type__app_label="auth", codename="view_user"))
        self.assertEqual(self.admin_post(unprivileged_staff, target_path, data).status_code, 403)
        self.assertEqual(self.admin_post(self.hunter, target_path, data).status_code, 302)
        self.assertEqual(self.admin_post(self.support, target_path, data, csrf=False).status_code, 403)
        self.hunter.refresh_from_db()
        self.assertTrue(self.hunter.check_password(PASSWORD))
        hunter_browser = Client()
        hunter_browser.force_login(self.hunter)
        self.assertEqual(self.admin_post(self.support, target_path, data).status_code, 302)
        self.hunter.refresh_from_db()
        self.assertTrue(self.hunter.check_password(NEW_PASSWORD))
        self.assertEqual(hunter_browser.get("/api/auth/me/").status_code, 401)

    def test_support_cannot_modify_reset_or_delete_other_staff_or_delete_self_even_in_bulk(self):
        for target in [self.administrator, User.objects.create_user(username="peer_support", password=PASSWORD, is_staff=True)]:
            for suffix in ["change/", "password/", "delete/"]:
                response = self.admin_post(self.support, f"/admin/auth/user/{target.pk}/{suffix}", {"post": "yes", "password1": NEW_PASSWORD, "password2": NEW_PASSWORD})
                self.assertEqual(response.status_code, 403)
            response = self.admin_post(self.support, "/admin/auth/user/", {"action": "delete_selected", "_selected_action": [target.pk], "post": "yes", "index": "0"})
            self.assertEqual(response.status_code, 403)
            target.refresh_from_db()
            self.assertTrue(target.check_password(PASSWORD))
        self.assertEqual(self.admin_post(self.support, f"/admin/auth/user/{self.support.pk}/delete/", {"post": "yes"}).status_code, 403)
        self.assertEqual(self.admin_post(self.support, "/admin/auth/user/", {"action": "delete_selected", "_selected_action": [self.support.pk], "post": "yes", "index": "0"}).status_code, 403)
        self.assertTrue(User.objects.filter(pk=self.support.pk).exists())

    def test_admin_account_deletion_cascades_only_owner_data_and_preserves_reviewed_publications(self):
        species = Species.objects.create(common_name="Synthetic account-deletion species")
        land = LandType.objects.create(name="Private Land")
        preference = UserPreference.objects.create(user=self.hunter)
        preference.species.add(species)
        UserLicense.objects.create(user=self.hunter, name="Owned license")
        SavedSearch.objects.create(user=self.hunter, species=species, land_type=land, hunting_date=date(2026, 10, 12))
        Harvest.objects.create(user=self.hunter, species=species, harvest_date=timezone.localdate(), location="Private owned location")
        other = User.objects.create_user(username="untouched_hunter", password=PASSWORD)
        untouched = UserLicense.objects.create(user=other, name="Other user's license")
        self.hunter.is_staff = True
        self.hunter.save(update_fields=["is_staff"])
        self.hunter.user_permissions.add(Permission.objects.get(content_type__app_label="integration", codename="publish_regulationdraft"))
        source_url = "https://myfwc.com/synthetic-account-deletion-unit-test/"
        draft = RegulationDraft.objects.create(
            key="account-deletion-test", title="Synthetic deletion test", species=species, land_type=land,
            payload={"version": 1, "species_id": species.pk, "land_type_id": land.pk,
                     "coverage": {"start_date": "2026-01-01", "end_date": "2026-12-31"},
                     "sources": [{"url": source_url, "title": "Synthetic unit-test source", "checked_on": timezone.localdate().isoformat(), "evidence": "Synthetic test evidence, not hunting guidance."}],
                     "rules": [{"name": "Synthetic season", "code": "TEST", "category": "Synthetic category", "bag": "Synthetic bag guidance", "licenses": "Synthetic license guidance", "methods": "Synthetic method guidance",
                                "periods": [{"start_date": "2026-01-01", "end_date": "2026-12-31"}], "source_urls": [source_url]}]},
        )
        publication = draft.publish(reviewer=self.hunter, sources_checked=True, review_notes="Synthetic test publication")
        snapshot = publication.snapshot
        owner_id = self.hunter.pk
        hunter_browser = Client()
        hunter_browser.force_login(self.hunter)
        response = self.admin_post(self.administrator, f"/admin/auth/user/{owner_id}/delete/", {"post": "yes"})
        self.assertEqual(response.status_code, 302, response.content)
        self.assertFalse(User.objects.filter(pk=owner_id).exists())
        for model in [UserPreference, UserLicense, SavedSearch, Harvest]:
            self.assertFalse(model.objects.filter(user_id=owner_id).exists())
        self.assertTrue(UserLicense.objects.filter(pk=untouched.pk, user=other).exists())
        self.assertTrue(Species.objects.filter(pk=species.pk).exists())
        publication = RegulatoryPublication.objects.get(pk=publication.pk)
        self.assertIsNone(publication.reviewed_by_id)
        self.assertEqual(publication.snapshot, snapshot)
        self.assertTrue(publication.is_current)
        result = Client().get("/api/regulations/search/", {"species": species.pk, "land_type": land.pk, "date": "2026-10-12"})
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.json()["verified"])
        self.assertEqual(hunter_browser.get("/api/auth/me/").status_code, 401)
