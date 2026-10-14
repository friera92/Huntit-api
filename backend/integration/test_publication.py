import json
from copy import deepcopy
from datetime import date
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management import call_command
from django.test import TestCase

from regulations.models import (
    DeerManagementUnit, HuntingSeason, HuntingZone, LandType, ManagedArea,
    SeasonPeriod, SeasonType, Source, Species,
)
from .models import RegulationDraft, RegulatoryPublication, validate_payload
from .starter import CORBETT, DEER, HOG, PYTHON, PYTHON_AREAS, seed_review_drafts


class ReviewedComplianceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_review_drafts()
        cls.reviewer = get_user_model().objects.create_superuser(
            username="reviewer", email="reviewer@example.invalid", password="Review-test-strong-642!"
        )
        cls.private = LandType.objects.get(name="Private Land")
        cls.public = LandType.objects.get(name="Commission-Managed Land")
        cls.wma = LandType.objects.get(name="Wildlife Management Area (WMA)")
        cls.hog = Species.objects.get(common_name="Wild Hog")
        cls.python = Species.objects.get(common_name="Burmese Python")
        cls.deer = Species.objects.get(common_name="White Tailed Deer")
        cls.corbett = ManagedArea.objects.get(name="J. W. Corbett WMA")

    def publish(self, key):
        return RegulationDraft.objects.get(key=key).publish(
            reviewer=self.reviewer, sources_checked=True, review_notes="Reviewed linked official scope, dates, exceptions and permits for this test."
        )

    def search(self, **overrides):
        params = {"species": self.hog.pk, "land_type": self.private.pk,
                  "date": "2026-10-12", "landowner_permission": "true"}
        params.update(overrides)
        return self.client.get("/api/regulations/search/", params)

    def test_fresh_setup_has_three_dated_source_linked_species_but_no_auto_approval(self):
        self.assertEqual(RegulationDraft.objects.values("species").distinct().count(), 3)
        self.assertEqual(RegulationDraft.objects.count(), 18)
        self.assertFalse(RegulatoryPublication.objects.exists())
        for draft in RegulationDraft.objects.all():
            draft.full_clean()
            self.assertTrue(draft.payload["sources"][0]["checked_on"])
            self.assertTrue(draft.payload["rules"][0]["periods"])
        result = self.search().json()
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["verified"])
        self.assertEqual(result["matched_seasons"], [])
        self.assertNotIn("No hunting license", result["licenses"])
        self.assertEqual(result["sources"][0]["url"], HOG)
        self.assertIsNone(result["sources"][0]["last_verified_at"])

    def test_hog_private_exception_permission_and_sources(self):
        pub = self.publish("hog-private-2026")
        result = self.search().json()
        self.assertTrue(result["verified"])
        self.assertEqual(result["status"], "reviewed")
        self.assertFalse(result["species_information_reviewed"])
        self.assertIn("No hunting license or nighttime gun-and-light permit", result["licenses"])
        self.assertIn("No size or bag limit", result["bag"])
        self.assertEqual(result["sources"][0]["last_verified_at"], pub.reviewed_at.isoformat())
        self.assertTrue(all(row["last_verified_at"] for row in result["matched_seasons"]))
        denied = self.search(landowner_permission="false").json()
        self.assertEqual(denied["eligibility"], "permission_required")
        self.assertIn("Do not hunt without it", " ".join(denied["alerts"]))

    def test_hog_private_exception_does_not_leak_to_public_land(self):
        self.publish("hog-private-2026")
        result = self.search(land_type=self.wma.pk, managed_area=self.corbett.pk).json()
        self.assertFalse(result["verified"])
        self.assertNotIn("No hunting license or nighttime", result["licenses"])

    def test_python_year_round_32_area_scope_anti_cruelty_and_live_transport(self):
        self.publish(f"python-public-{self.public.pk}-2026")
        result = self.search(species=self.python.pk, land_type=self.public.pk, managed_area=self.corbett.pk).json()
        self.assertEqual(len(PYTHON_AREAS), 32)
        self.assertTrue(result["verified"])
        self.assertIn("No hunting license", result["licenses"])
        self.assertIn("anti-cruelty", " ".join(result["alerts"]))
        self.assertIn("may not transport live", " ".join(result["alerts"]))
        self.assertIn("captive-bolt", result["methods"])
        self.assertIn("firearm/PCP air gun", result["methods"])
        self.assertIn("required second step", result["methods"])
        self.assertIn(PYTHON, [source["url"] for source in result["sources"]])
        outside = ManagedArea.objects.create(name="Other public land", area_type="OTHER")
        unsupported = self.search(species=self.python.pk, land_type=self.public.pk, managed_area=outside.pk).json()
        self.assertEqual(unsupported["status"], "no_data")
        self.assertFalse(unsupported["verified"])
        self.assertEqual(self.search(species=self.python.pk, land_type=self.public.pk).status_code, 400)

    def test_python_private_permission_required(self):
        self.publish("python-private-2026")
        result = self.search(species=self.python.pk, landowner_permission="false").json()
        self.assertEqual(result["eligibility"], "permission_required")
        self.assertIn("No bag limit", result["bag"])

    def test_year_round_coverage_bounds_are_explicit_and_review_expires(self):
        self.publish("hog-private-2026")
        for day in ["2026-01-01", "2026-12-31"]:
            with self.subTest(day=day):
                self.assertEqual(self.search(date=day).json()["status"], "reviewed")
        for day in ["2025-12-31", "2027-01-01"]:
            with self.subTest(day=day):
                result = self.search(date=day).json()
                self.assertFalse(result["verified"])
                self.assertEqual(result["status"], "no_data")

    def test_deer_requires_zone_and_dmu_and_rejects_mismatch(self):
        self.publish("deer-private-a2-2026-2027")
        result = self.search(species=self.deer.pk)
        self.assertEqual(result.status_code, 400)
        self.assertIn("zone", result.json())
        self.assertIn("dmu", result.json())
        zone_b = HuntingZone.objects.get(code="B")
        dmu_a = DeerManagementUnit.objects.get(code="A2")
        result = self.search(species=self.deer.pk, zone=zone_b.pk, dmu=dmu_a.pk)
        self.assertEqual(result.status_code, 400)
        self.assertIn("dmu", result.json())

    def test_deer_zone_dmu_date_filter_and_cross_year_season(self):
        self.publish("deer-private-a2-2026-2027")
        self.publish("deer-private-b1-2026-2027")
        a2, b1 = [DeerManagementUnit.objects.get(code=code) for code in ["A2", "B1"]]
        result = self.search(species=self.deer.pk, dmu=a2.pk).json()
        self.assertEqual(result["query"]["zone"], a2.zone_id)
        self.assertTrue(all(row["scopes"]["dmu"] == a2.pk for row in result["matched_seasons"]))
        self.assertIn("Daily 2", result["bag"])
        for day in ["2026-12-05", "2027-02-21"]:
            with self.subTest(day=day):
                self.assertEqual(self.search(species=self.deer.pk, dmu=b1.pk, date=day).json()["status"], "reviewed")
        closed = self.search(species=self.deer.pk, dmu=b1.pk, date="2027-02-22").json()
        self.assertEqual(closed["status"], "closed")
        self.assertEqual(closed["eligibility"], "no_open_season")
        self.assertEqual(closed["matched_seasons"], [])
        self.assertIn(DEER, [source["url"] for source in closed["sources"]])

    def test_antlerless_window_is_not_inferred_from_antlered_season(self):
        self.publish("deer-private-a2-2026-2027")
        a2 = DeerManagementUnit.objects.get(code="A2")
        opening = self.search(species=self.deer.pk, dmu=a2.pk, date="2026-11-21").json()
        after = self.search(species=self.deer.pk, dmu=a2.pk, date="2026-11-23").json()
        self.assertTrue(any("Antlerless" in row["category"] for row in opening["matched_seasons"]))
        self.assertFalse(any("Antlerless" in row["category"] for row in after["matched_seasons"]))

    def test_corbett_uses_area_dates_bag_and_permits_instead_of_private_schedule(self):
        self.publish(f"deer-corbett-{self.wma.pk}-2026-2027")
        result = self.search(species=self.deer.pk, land_type=self.wma.pk, managed_area=self.corbett.pk).json()
        self.assertEqual(result["status"], "reviewed")
        self.assertIn("2026-10-03 to 2026-10-18", result["dates"])
        self.assertIn("Area daily limit 1", result["bag"])
        self.assertIn("area annual limit 2", result["bag"])
        self.assertIn("management area permit", result["licenses"])
        self.assertIn("Muzzleloading gun season permit", result["licenses"])
        self.assertIn("Bruce Bowman", result["methods"])
        self.assertIn(CORBETT, [source["url"] for source in result["sources"]])
        other = ManagedArea.objects.get(name="Big Cypress WMA")
        self.assertFalse(self.search(species=self.deer.pk, land_type=self.wma.pk, managed_area=other.pk).json()["verified"])

    def test_draft_edits_do_not_change_published_answer_until_new_review(self):
        first = self.publish("hog-private-2026")
        draft = first.draft
        draft.payload["rules"][0]["bag"] = "Changed draft bag for a later review."
        draft.save()
        result = self.search().json()
        self.assertIn("No size or bag limit", result["bag"])
        self.assertNotIn("Changed draft", result["bag"])
        second = self.publish("hog-private-2026")
        self.assertIn("Changed draft", self.search().json()["bag"])
        self.assertEqual(second.revision, 2)
        first.refresh_from_db()
        self.assertFalse(first.is_current)
        self.assertEqual(RegulatoryPublication.objects.filter(is_current=True).count(), 1)
        first.snapshot["rules"][0]["bag"] = "Mutation"
        with self.assertRaises(ValidationError):
            first.save()

    def test_draft_identity_edits_cannot_reassign_a_published_snapshot(self):
        pub = self.publish("hog-private-2026")
        pub.draft.species = self.python
        pub.draft.payload["species_id"] = self.python.pk
        pub.draft.save()
        self.assertTrue(self.search().json()["verified"])
        self.assertFalse(self.search(species=self.python.pk).json()["verified"])

    def test_catalog_coverage_and_identity_use_approved_snapshot_until_another_review(self):
        pub = self.publish("hog-private-2026")
        draft = pub.draft
        original_title = draft.title
        draft.title = "Unreviewed changed title"
        draft.species = self.python
        draft.land_type = self.public
        draft.payload["species_id"] = self.python.pk
        draft.payload["land_type_id"] = self.public.pk
        draft.payload["coverage"] = {"start_date": "2030-01-01", "end_date": "2030-12-31"}
        draft.payload["scopes"] = {"zone": HuntingZone.objects.get(code="B").pk}
        draft.save()
        catalog = self.client.get("/api/catalog/").json()
        reviewed = [row for row in catalog["supported_scopes"] if row["reviewed"]]
        self.assertEqual(len(reviewed), 1)
        self.assertEqual(reviewed[0], {"title": original_title, "species": self.hog.pk,
            "land_type": self.private.pk, "coverage": {"start_date": "2026-01-01", "end_date": "2026-12-31"},
            "scopes": {}, "reviewed": True})

    def test_imported_record_changes_never_auto_publish(self):
        self.publish("hog-private-2026")
        source = Source.objects.create(organization="FWC", title="Unreviewed import", url=HOG)
        season_type = SeasonType.objects.create(name="Unreviewed season", code="UNREVIEWED")
        season = HuntingSeason.objects.create(species=self.hog, land_type=self.private,
            season_type=season_type, season_year="2026-2027", daily_bag_limit=9, source=source, notes="Unreviewed imported claim")
        SeasonPeriod.objects.create(season=season, start_date=date(2026, 10, 1), end_date=date(2026, 10, 31))
        result = self.search().json()
        self.assertNotIn("Unreviewed imported", " ".join(result["alerts"]))
        self.assertNotIn("9", result["bag"])
        self.assertNotIn("Unreviewed season", result["dates"])

    def test_repeated_seed_does_not_replace_drafts_or_publish_them(self):
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        draft.payload["rules"][0]["bag"] = "Team-maintained working edit"
        draft.save()
        self.assertEqual(seed_review_drafts(), 0)
        draft.refresh_from_db()
        self.assertEqual(draft.payload["rules"][0]["bag"], "Team-maintained working edit")
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_incomplete_or_unofficial_source_and_bad_dates_block_publication(self):
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        original = deepcopy(draft.payload)
        invalid = [lambda p: p["sources"][0].update(url="https://untrusted.example/"),
                   lambda p: p["sources"][0].update(checked_on="2099-01-01"),
                   lambda p: p["rules"][0]["periods"][0].update(end_date="2025-01-01"),
                   lambda p: p["rules"][0].update(source_urls=[])]
        for change in invalid:
            with self.subTest(change=change):
                draft.payload = deepcopy(original)
                change(draft.payload)
                draft.save()
                with self.assertRaises(ValidationError):
                    self.publish(draft.key)
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_admin_review_requires_permission_acknowledgement_and_notes(self):
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        ordinary = get_user_model().objects.create_user(username="ordinary")
        staff = get_user_model().objects.create_user(username="staff", is_staff=True)
        for user in [ordinary, staff]:
            with self.subTest(user=user.username), self.assertRaises(PermissionDenied):
                draft.publish(reviewer=user, sources_checked=True, review_notes="Checked")
        for checked, notes in [(False, "checked"), (True, "")]:
            with self.subTest(checked=checked, notes=notes), self.assertRaises(ValidationError):
                draft.publish(reviewer=self.reviewer, sources_checked=checked, review_notes=notes)

    def test_admin_publish_form_enforces_explicit_review_and_snapshot_is_read_only(self):
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        path = f"/admin/integration/regulationdraft/{draft.pk}/change/"
        self.assertEqual(self.client.get(path).status_code, 302)
        self.client.force_login(self.reviewer)
        post = {"key": draft.key, "title": draft.title, "species": draft.species_id,
                "land_type": draft.land_type_id, "payload": json.dumps(draft.payload), "_publish": "yes"}
        invalid = self.client.post(path, post)
        self.assertEqual(invalid.status_code, 200)
        self.assertContains(invalid, "Check the source acknowledgement")
        self.assertFalse(RegulatoryPublication.objects.exists())
        post.update(sources_checked="on", review_notes="Checked all linked source facts and restrictions.")
        self.assertEqual(self.client.post(path, post).status_code, 302)
        published = RegulatoryPublication.objects.get()
        self.assertEqual(self.client.post(f"/admin/integration/regulatorypublication/{published.pk}/change/", {"snapshot": "{}"}).status_code, 403)

    def test_staff_with_edit_permission_cannot_publish_without_review_permission(self):
        staff = get_user_model().objects.create_user(username="drafteditor", is_staff=True)
        staff.user_permissions.add(Permission.objects.get(codename="change_regulationdraft", content_type__app_label="integration"))
        self.client.force_login(staff)
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        post = {"key": draft.key, "title": draft.title, "species": draft.species_id,
                "land_type": draft.land_type_id, "payload": json.dumps(draft.payload),
                "_publish": "yes", "sources_checked": "on", "review_notes": "Checked"}
        response = self.client.post(f"/admin/integration/regulationdraft/{draft.pk}/change/", post)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "do not have regulatory publication permission")
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_arbitrary_json_types_are_validation_errors_and_not_server_errors(self):
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        original = deepcopy(draft.payload)
        changes = [lambda p: p.update(coverage=None), lambda p: p.update(sources=["text"]),
                   lambda p: p.update(rules=[None]), lambda p: p["rules"][0].update(periods=None),
                   lambda p: p["rules"][0].update(periods=[None]), lambda p: p.update(alerts=[{}]),
                   lambda p: p.update(required_inputs=[{}]), lambda p: p.update(scopes={"dmu": None}),
                   lambda p: p["sources"][0].update(url=[]), lambda p: p["rules"][0].update(source_urls={"bad": True})]
        self.client.force_login(self.reviewer)
        for change in changes:
            broken = deepcopy(original)
            change(broken)
            with self.subTest(broken=broken), self.assertRaises(ValidationError):
                validate_payload(broken)
            post = {"key": draft.key, "title": draft.title, "species": draft.species_id,
                    "land_type": draft.land_type_id, "payload": json.dumps(broken), "_publish": "yes",
                    "sources_checked": "on", "review_notes": "Checked"}
            with self.subTest(admin_payload=broken):
                self.assertEqual(self.client.post(f"/admin/integration/regulationdraft/{draft.pk}/change/", post).status_code, 200)
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_publications_cannot_be_created_by_bypassing_the_review_method(self):
        draft = RegulationDraft.objects.get(key="hog-private-2026")
        with self.assertRaises(PermissionDenied):
            RegulatoryPublication.objects.create(draft=draft, revision=1, snapshot=draft.payload,
                reviewed_by=self.reviewer, reviewed_at="2026-10-12T12:00:00Z", review_notes="Bypassed", is_current=True)
        self.assertFalse(RegulatoryPublication.objects.exists())

    def test_dmu_zone_conflicts_and_rule_scope_escape_block_review(self):
        draft = RegulationDraft.objects.get(key="deer-private-a2-2026-2027")
        broken = deepcopy(draft.payload)
        broken["scopes"]["zone"] = HuntingZone.objects.get(code="B").pk
        with self.assertRaisesMessage(ValidationError, "DMU must belong"):
            validate_payload(broken)
        broken = deepcopy(draft.payload)
        broken["rules"][0]["scopes"]["dmu"] = DeerManagementUnit.objects.get(code="B1").pk
        with self.assertRaisesMessage(ValidationError, "cannot extend outside"):
            validate_payload(broken)

    def test_authorized_admin_can_withdraw_but_keeps_review_history(self):
        publication = self.publish("hog-private-2026")
        self.client.force_login(self.reviewer)
        response = self.client.post("/admin/integration/regulationdraft/", {
            "action": "withdraw_publication", "_selected_action": str(publication.draft_id), "index": "0"})
        self.assertEqual(response.status_code, 302)
        publication.refresh_from_db()
        self.assertFalse(publication.is_current)
        self.assertTrue(RegulatoryPublication.objects.filter(pk=publication.pk).exists())
        self.assertEqual(self.search().json()["status"], "needs_review")
