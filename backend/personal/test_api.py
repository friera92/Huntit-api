import json
from copy import deepcopy
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.utils import timezone

from integration.models import RegulationDraft

from regulations.models import (
    DeerManagementUnit, HuntingSeason, HuntingZone, LandType, LicensePermit,
    ManagedArea, SeasonPeriod, SeasonType, Source, Species,
)

from .models import Harvest, SavedSearch, UserLicense, UserPreference


PASSWORD = "Personal-API-test-passphrase-836!"


class PersonalAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="owner", password=PASSWORD)
        cls.other = get_user_model().objects.create_user(username="other", password=PASSWORD)
        cls.species = Species.objects.create(common_name="Synthetic species")
        cls.retired_species = Species.objects.create(common_name="Retired species", is_active=False)
        cls.private = LandType.objects.create(name="Private Land")
        cls.public = LandType.objects.create(name="Wildlife Management Area (WMA)")
        cls.area = ManagedArea.objects.create(name="Synthetic area", area_type="WMA")
        cls.retired_area = ManagedArea.objects.create(name="Retired area", is_active=False)
        cls.zone_a = HuntingZone.objects.create(name="Zone A", code="A")
        cls.zone_b = HuntingZone.objects.create(name="Zone B", code="B")
        cls.dmu = DeerManagementUnit.objects.create(code="A1", zone=cls.zone_a)
        cls.permit = LicensePermit.objects.create(name="Synthetic permit")
        cls.retired_permit = LicensePermit.objects.create(name="Retired permit", is_active=False)
        cls.source = Source.objects.create(organization="Synthetic", title="Test source", url="https://example.invalid/source")
        cls.season_type = SeasonType.objects.create(name="Test season", code="TEST")
        cls.season = HuntingSeason.objects.create(
            species=cls.species, land_type=cls.private, season_type=cls.season_type,
            season_year="2026", source=cls.source, notes="Original test rule",
        )
        SeasonPeriod.objects.create(season=cls.season, start_date=date(2026, 1, 1), end_date=date(2026, 12, 31))

    def setUp(self):
        cache.clear()
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.owner)

    def mutate(self, method, path, data=None, *, csrf=True):
        headers = {}
        if csrf:
            self.client.get("/api/auth/csrf/")
            headers["HTTP_X_CSRFTOKEN"] = self.client.cookies["csrftoken"].value
        return getattr(self.client, method)(path, json.dumps(data or {}), content_type="application/json", **headers)

    def search_data(self, **extra):
        data = {"title": "My plan", "species": self.species.pk, "land_type": self.private.pk,
                "hunting_date": "2026-10-12", "landowner_permission": True}
        data.update(extra)
        return data

    def harvest_data(self, **extra):
        data = {"species": self.species.pk, "harvest_date": timezone.localdate().isoformat(),
                "location": "Synthetic private property", "quantity": 1, "notes": "Personal test note"}
        data.update(extra)
        return data

    def endpoint_records(self, owner):
        return [
            ("licenses", UserLicense.objects.create(user=owner, name="Personal license")),
            ("harvests", Harvest.objects.create(user=owner, species=self.species, harvest_date=timezone.localdate(), location="Personal site")),
            ("saved-searches", SavedSearch.objects.create(user=owner, species=self.species, land_type=self.private, hunting_date=date(2026, 10, 12))),
        ]

    def test_all_personal_endpoints_require_sign_in(self):
        records = self.endpoint_records(self.owner)
        self.client.logout()
        for method, path in [("get", "/api/personal/preferences/"), ("put", "/api/personal/preferences/")]:
            response = self.client.get(path) if method == "get" else self.mutate(method, path)
            self.assertEqual(response.status_code, 403)
        for resource, record in records:
            base = f"/api/personal/{resource}/"
            for method, path in [("get", base), ("post", base), ("get", f"{base}{record.pk}/"),
                                 ("patch", f"{base}{record.pk}/"), ("delete", f"{base}{record.pk}/")]:
                with self.subTest(method=method, path=path):
                    response = self.client.get(path) if method == "get" else self.mutate(method, path)
                    self.assertEqual(response.status_code, 403)
        self.assertEqual(self.client.get(f"/api/personal/saved-searches/{records[-1][1].pk}/run/").status_code, 403)

    def test_every_detail_operation_is_owner_scoped_and_lists_exclude_other_users(self):
        others = self.endpoint_records(self.other)
        mine = self.endpoint_records(self.owner)
        for (resource, other_record), (_, my_record) in zip(others, mine):
            base = f"/api/personal/{resource}/"
            self.assertEqual([row["id"] for row in self.client.get(base).json()], [my_record.pk])
            for method in ["get", "patch", "delete"]:
                with self.subTest(resource=resource, operation=method):
                    response = self.client.get(f"{base}{other_record.pk}/") if method == "get" else self.mutate(method, f"{base}{other_record.pk}/", {"notes": "Intrusion"})
                    self.assertEqual(response.status_code, 404)
                    other_record.refresh_from_db()
                    self.assertNotEqual(getattr(other_record, "notes", ""), "Intrusion")
        self.assertEqual(self.client.get(f"/api/personal/saved-searches/{others[-1][1].pk}/run/").status_code, 404)

    def test_records_create_edit_persist_after_real_logout_login_and_delete(self):
        cases = [
            ("licenses", {"permit": self.permit.pk, "name": "My license", "status": "held", "valid_from": "2026-01-01", "expires_on": "2026-12-31"}, {"status": "expired"}),
            ("harvests", self.harvest_data(), {"quantity": 3, "notes": "Edited note"}),
            ("saved-searches", self.search_data(), {"title": "Updated plan", "landowner_permission": False}),
        ]
        created = []
        for resource, data, patch in cases:
            response = self.mutate("post", f"/api/personal/{resource}/", data)
            self.assertEqual(response.status_code, 201, response.content)
            self.assertNotIn("user", response.json())
            path = f"/api/personal/{resource}/{response.json()['id']}/"
            self.assertEqual(self.mutate("patch", path, patch).status_code, 200)
            created.append((path, patch))
        self.assertEqual(self.mutate("post", "/api/auth/logout/").status_code, 204)
        self.assertEqual(self.mutate("post", "/api/auth/login/", {"username": "owner", "password": PASSWORD}).status_code, 200)
        for path, patch in created:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            for name, value in patch.items():
                self.assertEqual(response.json()[name], value)
            self.assertEqual(self.mutate("delete", path).status_code, 204)
            self.assertEqual(self.client.get(path).status_code, 404)
        self.assertEqual(UserLicense.objects.count() + Harvest.objects.count() + SavedSearch.objects.count(), 0)

    def test_preferences_are_persistent_and_owner_isolated_without_get_side_effects(self):
        self.assertEqual(self.client.get("/api/personal/preferences/").json(), {"species": [], "managed_areas": [], "zones": []})
        self.assertFalse(UserPreference.objects.exists())
        data = {"species": [self.species.pk], "managed_areas": [self.area.pk], "zones": [self.zone_a.pk]}
        self.assertEqual(self.mutate("put", "/api/personal/preferences/", data).json(), data)
        preference_id = UserPreference.objects.get(user=self.owner).pk
        self.client.logout()
        self.client.force_login(self.other)
        self.assertEqual(self.client.get("/api/personal/preferences/").json(), {"species": [], "managed_areas": [], "zones": []})
        self.client.logout()
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get("/api/personal/preferences/").json(), data)
        invalid = {**data, "species": [self.retired_species.pk]}
        self.assertEqual(self.mutate("put", "/api/personal/preferences/", invalid).status_code, 400)
        self.assertEqual(self.client.get("/api/personal/preferences/").json(), data)
        self.assertEqual(self.mutate("put", "/api/personal/preferences/", {"species": [], "managed_areas": [], "zones": []}).status_code, 200)
        self.assertEqual(UserPreference.objects.get(user=self.owner).pk, preference_id)
        self.assertEqual(UserPreference.objects.filter(user=self.owner).count(), 1)

    def test_owner_cannot_be_selected_or_changed_in_request_data(self):
        for resource, data in [("licenses", {"name": "License"}), ("harvests", self.harvest_data()), ("saved-searches", self.search_data())]:
            for field in ["user", "user_id"]:
                self.assertEqual(self.mutate("post", f"/api/personal/{resource}/", {**data, field: self.other.pk}).status_code, 400)
        for resource, record in self.endpoint_records(self.owner):
            self.assertEqual(self.mutate("patch", f"/api/personal/{resource}/{record.pk}/", {"user": self.other.pk}).status_code, 400)
            record.refresh_from_db()
            self.assertEqual(record.user_id, self.owner.pk)
        self.assertEqual(self.mutate("put", "/api/personal/preferences/", {"species": [], "managed_areas": [], "zones": [], "user": self.other.pk}).status_code, 400)

    def test_csrf_is_required_for_every_personal_mutation(self):
        self.assertEqual(self.mutate("put", "/api/personal/preferences/", {"species": [], "managed_areas": [], "zones": []}, csrf=False).status_code, 403)
        for resource, record in self.endpoint_records(self.owner):
            for method, path in [("post", f"/api/personal/{resource}/"), ("patch", f"/api/personal/{resource}/{record.pk}/"), ("delete", f"/api/personal/{resource}/{record.pk}/")]:
                self.assertEqual(self.mutate(method, path, {"notes": "Unsafe change"}, csrf=False).status_code, 403)
            record.refresh_from_db()
            self.assertNotEqual(getattr(record, "notes", ""), "Unsafe change")

    def test_license_validation_handles_dates_status_blank_name_and_inactive_permit(self):
        for data in [
            {"name": "License", "valid_from": "2026-12-31", "expires_on": "2026-01-01"},
            {"name": "License", "status": "officially_verified"}, {"name": " "},
            {"name": "License", "permit": self.retired_permit.pk},
        ]:
            with self.subTest(data=data):
                self.assertEqual(self.mutate("post", "/api/personal/licenses/", data).status_code, 400)
        self.assertFalse(UserLicense.objects.exists())

    def test_harvest_validation_and_display_fields(self):
        for data in [self.harvest_data(location=" "), self.harvest_data(quantity=0),
                     self.harvest_data(harvest_date=(timezone.localdate() + timedelta(days=1)).isoformat()),
                     self.harvest_data(species=self.retired_species.pk), self.harvest_data(managed_area=self.retired_area.pk)]:
            with self.subTest(data=data):
                self.assertEqual(self.mutate("post", "/api/personal/harvests/", data).status_code, 400)
        response = self.mutate("post", "/api/personal/harvests/", self.harvest_data(location="", managed_area=self.area.pk))
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()["species_name"], self.species.common_name)
        self.assertEqual(response.json()["managed_area_name"], self.area.name)
        self.assertIn("species_image", response.json())

    def test_saved_search_validates_geography_active_records_and_infers_dmu_zone(self):
        for data in [self.search_data(land_type=self.public.pk), self.search_data(managed_area=self.area.pk),
                     self.search_data(zone=self.zone_b.pk, dmu=self.dmu.pk),
                     self.search_data(species=self.retired_species.pk),
                     self.search_data(land_type=self.public.pk, managed_area=self.retired_area.pk)]:
            with self.subTest(data=data):
                self.assertEqual(self.mutate("post", "/api/personal/saved-searches/", data).status_code, 400)
        response = self.mutate("post", "/api/personal/saved-searches/", self.search_data(dmu=self.dmu.pk))
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()["zone"], self.zone_a.pk)

    def test_partial_update_revalidates_combined_old_and_new_fields(self):
        response = self.mutate("post", "/api/personal/licenses/", {"name": "License", "valid_from": "2026-06-01"})
        path = f"/api/personal/licenses/{response.json()['id']}/"
        self.assertEqual(self.mutate("patch", path, {"expires_on": "2026-05-01"}).status_code, 400)
        self.assertIsNone(UserLicense.objects.get().expires_on)
        response = self.mutate("post", "/api/personal/saved-searches/", self.search_data())
        path = f"/api/personal/saved-searches/{response.json()['id']}/"
        self.assertEqual(self.mutate("patch", path, {"land_type": self.public.pk}).status_code, 400)
        self.assertEqual(SavedSearch.objects.get().land_type_id, self.private.pk)

    def test_malformed_json_shapes_are_validation_errors_for_create_patch_and_preferences(self):
        self.client.get("/api/auth/csrf/")
        headers = {"HTTP_X_CSRFTOKEN": self.client.cookies["csrftoken"].value}
        endpoints = [("PUT", "/api/personal/preferences/")]
        for resource, record in self.endpoint_records(self.owner):
            endpoints += [("POST", f"/api/personal/{resource}/"), ("PATCH", f"/api/personal/{resource}/{record.pk}/")]
        for method, path in endpoints:
            for data in [None, 4, True, "unexpected", []]:
                with self.subTest(method=method, path=path, data=data):
                    response = self.client.generic(method, path, json.dumps(data), content_type="application/json", **headers)
                    self.assertEqual(response.status_code, 400, response.content)

    def test_personal_dispatch_marks_inputs_sensitive_for_debug_reports(self):
        responses = [
            self.mutate("put", "/api/personal/preferences/", {"species": [], "managed_areas": [], "zones": []}),
            self.mutate("post", "/api/personal/licenses/", {"name": "Private license", "notes": "Private notes"}),
            self.mutate("post", "/api/personal/harvests/", self.harvest_data()),
            self.mutate("post", "/api/personal/saved-searches/", self.search_data()),
        ]
        for response in responses:
            self.assertIn(response.status_code, [200, 201], response.content)
            self.assertEqual(response.wsgi_request.sensitive_post_parameters, "__ALL__")

    def test_harvest_archive_and_restore_are_recoverable_idempotent_and_owner_scoped(self):
        mine = self.endpoint_records(self.owner)[1][1]
        other = self.endpoint_records(self.other)[1][1]
        path = f"/api/personal/harvests/{mine.pk}/"
        archived = self.mutate("post", path + "archive/")
        self.assertEqual(archived.status_code, 200)
        self.assertIsNotNone(archived.json()["archived_at"])
        self.assertEqual(self.client.get("/api/personal/harvests/").json(), [])
        self.assertEqual([row["id"] for row in self.client.get("/api/personal/harvests/?archived=true").json()], [mine.pk])
        repeated = self.mutate("post", path + "archive/")
        self.assertEqual(repeated.json()["archived_at"], archived.json()["archived_at"])
        self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.mutate("patch", path, {"notes": "Still editable"}).status_code, 200)
        for action in ["archive", "restore"]:
            self.assertEqual(self.mutate("post", f"/api/personal/harvests/{other.pk}/{action}/").status_code, 404)
        other.refresh_from_db()
        self.assertIsNone(other.archived_at)
        restored = self.mutate("post", path + "restore/")
        self.assertEqual(restored.status_code, 200)
        self.assertIsNone(restored.json()["archived_at"])
        self.assertEqual(self.mutate("post", path + "restore/").status_code, 200)
        self.assertEqual([row["id"] for row in self.client.get("/api/personal/harvests/?archived=false").json()], [mine.pk])
        self.assertEqual(self.client.get("/api/personal/harvests/?archived=maybe").status_code, 400)
        self.assertEqual(self.mutate("post", path + "archive/").status_code, 200)
        self.assertEqual(self.mutate("delete", path).status_code, 204)
        self.assertFalse(Harvest.objects.filter(pk=mine.pk).exists())

    def reset_data(self, **extra):
        data = {"preferences": True, "saved_searches": True, "licenses": True,
                "harvests": "archive", "confirmation": "RESET MY DATA"}
        data.update(extra)
        return data

    def test_export_includes_all_own_records_and_no_authentication_secrets_or_other_users(self):
        mine = self.endpoint_records(self.owner)
        others = self.endpoint_records(self.other)
        pref = UserPreference.objects.create(user=self.owner)
        pref.species.add(self.species)
        UserPreference.objects.create(user=self.other)
        self.mutate("post", f"/api/personal/harvests/{mine[1][1].pk}/archive/")
        response = self.client.get("/api/personal/export/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment; filename="HuntIt-personal-data.json"', response["Content-Disposition"])
        data = response.json()
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["preferences"]["species"], [self.species.pk])
        for key, mine_record, other_record in [
            ("licenses", mine[0][1], others[0][1]), ("harvests", mine[1][1], others[1][1]),
            ("saved_searches", mine[2][1], others[2][1]),
        ]:
            self.assertEqual([row["id"] for row in data[key]], [mine_record.pk])
            self.assertNotIn(other_record.pk, [row["id"] for row in data[key]])
        self.assertIsNotNone(data["harvests"][0]["archived_at"])
        for secret in ["password", "sessionid", "csrftoken", self.owner.password, "user_id"]:
            self.assertNotIn(secret, response.content.decode())

    def test_reset_selected_personal_data_preserves_other_user_catalog_and_recoverable_harvests(self):
        mine = self.endpoint_records(self.owner)
        others = self.endpoint_records(self.other)
        preference = UserPreference.objects.create(user=self.owner)
        preference.species.add(self.species)
        UserPreference.objects.create(user=self.other)
        response = self.mutate("post", "/api/personal/reset/", self.reset_data())
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.json(), {"preferences": 1, "saved_searches": 1, "licenses": 1, "harvests_archived": 1})
        self.assertFalse(UserPreference.objects.filter(user=self.owner).exists())
        self.assertFalse(UserLicense.objects.filter(user=self.owner).exists())
        self.assertFalse(SavedSearch.objects.filter(user=self.owner).exists())
        harvest = Harvest.objects.get(pk=mine[1][1].pk)
        self.assertIsNotNone(harvest.archived_at)
        self.assertEqual(self.mutate("post", f"/api/personal/harvests/{harvest.pk}/restore/").status_code, 200)
        harvest.refresh_from_db()
        self.assertIsNone(harvest.archived_at)
        for _, record in others:
            record.refresh_from_db()
            self.assertEqual(record.user_id, self.other.pk)
        self.assertTrue(UserPreference.objects.filter(user=self.other).exists())
        self.assertTrue(Species.objects.filter(pk=self.species.pk).exists())
        self.assertTrue(HuntingSeason.objects.filter(pk=self.season.pk).exists())
        repeat = self.mutate("post", "/api/personal/reset/", self.reset_data(harvests="keep"))
        self.assertEqual(repeat.json(), {"preferences": 0, "saved_searches": 0, "licenses": 0, "harvests_archived": 0})

    def test_reset_validates_confirmation_and_flags_and_can_keep_selected_categories(self):
        self.endpoint_records(self.owner)
        UserPreference.objects.create(user=self.owner)
        for data in [self.reset_data(confirmation="RESET"), self.reset_data(harvests="delete"),
                     self.reset_data(licenses="maybe"), self.reset_data(user=self.other.pk), {}]:
            self.assertEqual(self.mutate("post", "/api/personal/reset/", data).status_code, 400)
            self.assertEqual(UserLicense.objects.filter(user=self.owner).count(), 1)
            self.assertEqual(SavedSearch.objects.filter(user=self.owner).count(), 1)
            self.assertEqual(Harvest.objects.filter(user=self.owner, archived_at__isnull=True).count(), 1)
        response = self.mutate("post", "/api/personal/reset/", self.reset_data(preferences=False, saved_searches=False, harvests="keep"))
        self.assertEqual(response.json(), {"preferences": 0, "saved_searches": 0, "licenses": 1, "harvests_archived": 0})
        self.assertTrue(UserPreference.objects.filter(user=self.owner).exists())
        self.assertTrue(SavedSearch.objects.filter(user=self.owner).exists())
        self.assertEqual(Harvest.objects.filter(user=self.owner, archived_at__isnull=True).count(), 1)

    def test_archive_restore_and_reset_require_csrf_and_all_controls_require_sign_in(self):
        mine = self.endpoint_records(self.owner)[1][1]
        paths = [f"/api/personal/harvests/{mine.pk}/archive/", f"/api/personal/harvests/{mine.pk}/restore/", "/api/personal/reset/"]
        for path in paths:
            self.assertEqual(self.mutate("post", path, self.reset_data(), csrf=False).status_code, 403)
        mine.refresh_from_db()
        self.assertIsNone(mine.archived_at)
        self.client.logout()
        for path in paths:
            self.assertEqual(self.mutate("post", path, self.reset_data()).status_code, 403)
        self.assertEqual(self.client.get("/api/personal/export/").status_code, 403)

    def test_saved_run_uses_current_reviewed_snapshot_not_changed_imports_or_drafts(self):
        source_url = "https://myfwc.com/synthetic-unit-test/"
        payload = {
            "version": 1, "species_id": self.species.pk, "land_type_id": self.private.pk,
            "coverage": {"start_date": "2026-01-01", "end_date": "2026-12-31"},
            "sources": [{"url": source_url, "title": "Synthetic unit-test source", "checked_on": timezone.localdate().isoformat(), "evidence": "Synthetic test evidence, not real hunting guidance."}],
            "rules": [{"name": "Synthetic test season", "code": "TEST", "category": "Synthetic category",
                       "bag": "Original reviewed limit", "licenses": "Synthetic license guidance", "methods": "Synthetic method guidance",
                       "periods": [{"start_date": "2026-01-01", "end_date": "2026-12-31"}], "source_urls": [source_url]}],
        }
        draft = RegulationDraft.objects.create(key="personal-api-test", title="Synthetic test draft", species=self.species, land_type=self.private, payload=payload)
        response = self.mutate("post", "/api/personal/saved-searches/", self.search_data())
        path = f"/api/personal/saved-searches/{response.json()['id']}/run/"
        first = self.client.get(path)
        self.assertEqual(first.status_code, 200, first.content)
        self.assertEqual(first.json()["status"], "needs_review")
        self.assertNotIn("Original test rule", first.json()["alerts"])
        reviewer = get_user_model().objects.create_superuser(username="test_reviewer", email="reviewer@example.invalid", password=PASSWORD)
        draft.publish(reviewer=reviewer, sources_checked=True, review_notes="Synthetic test publication")
        reviewed = self.client.get(path).json()
        self.assertIn("Original reviewed limit", reviewed["bag"])
        self.assertTrue(first.json()["query"]["landowner_permission"])
        HuntingSeason.objects.filter(pk=self.season.pk).update(notes="Changed current rule")
        draft.payload = deepcopy(draft.payload)
        draft.payload["rules"][0]["bag"] = "New reviewed limit"
        draft.save()
        unchanged = self.client.get(path).json()
        self.assertIn("Original reviewed limit", unchanged["bag"])
        self.assertNotIn("New reviewed limit", unchanged["bag"])
        self.assertNotIn("Changed current rule", unchanged["alerts"])
        draft.publish(reviewer=reviewer, sources_checked=True, review_notes="Synthetic revised publication")
        changed = self.client.get(path).json()
        self.assertIn("New reviewed limit", changed["bag"])
        self.assertNotIn("Original reviewed limit", changed["bag"])
        Species.objects.filter(pk=self.species.pk).update(is_active=False)
        self.assertEqual(self.client.get(path).status_code, 400)
        self.assertEqual(SavedSearch.objects.count(), 1)
