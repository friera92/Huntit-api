"""Public API boundary matrix over the installed human-approved release.

The complete distribution setup runs only inside Django's disposable database.
The matrix exercises the exact default publications without adding QA reviews.
"""
from datetime import date, timedelta
from io import StringIO
from urllib.parse import urlparse

from django.core.management import call_command
from django.test import TestCase

from regulations.models import HuntingZone, RegulatoryArea
from .models import RegulationDraft, RegulatoryPublication, SCOPE_MODELS


def _accepts(scopes, selections):
    for field, value in scopes.items():
        allowed = value if isinstance(value, list) else [value]
        if selections.get(field) is not None and selections[field] not in allowed:
            return False
    return True


def _contains(bounds, when):
    return (date.fromisoformat(bounds["start_date"]) <= when <= date.fromisoformat(bounds["end_date"])
            and ("weekdays" not in bounds or when.isoweekday() in bounds["weekdays"]))


class ExpansionPublicMatrixTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_local_data", stdout=StringIO(), verbosity=0)
        cls.original_publications = list(RegulatoryPublication.objects.filter(
            snapshot__approved_release__release_id="fwc-2026-10-12-v1"
        ).values("id", "snapshot", "revision"))
        cls.drafts = list(RegulationDraft.objects.order_by("pk"))
        cls.publications = list(RegulatoryPublication.objects.filter(is_current=True).order_by("pk"))

    def test_every_installed_period_boundary_has_exact_public_scope_and_date_matches(self):
        self.assertGreaterEqual(len(self.drafts), 54)
        self.assertEqual(len(self.publications), len(self.drafts))
        defaults = {field: model.objects.order_by("pk").first().pk for field, model in SCOPE_MODELS.items()}
        north = RegulatoryArea.objects.get(code="NORTH_SR70").pk
        zone_a = HuntingZone.objects.get(code="A").pk
        cases = {}
        periods_checked = 0
        for draft in self.drafts:
            for item in draft.payload["rules"]:
                scopes = {**draft.payload.get("scopes", {}), **item.get("scopes", {})}
                selections = {field: value[0] if isinstance(value, list) else value for field, value in scopes.items()}
                for field in draft.payload.get("required_inputs", []):
                    selections.setdefault(field, defaults[field])
                if "turkey" in draft.species.common_name.casefold() and "private" in draft.land_type.name.casefold():
                    # A before/after date can cross the fall/spring edition split.
                    # Both independent selectors keep that boundary request valid.
                    selections.setdefault("zone", zone_a)
                    selections.setdefault("regulatory_area", north)
                for bounds in item["periods"]:
                    periods_checked += 1
                    first, last = date.fromisoformat(bounds["start_date"]), date.fromisoformat(bounds["end_date"])
                    for when in [first - timedelta(days=1), first, last, last + timedelta(days=1)]:
                        params = {"species": draft.species_id, "land_type": draft.land_type_id,
                                  "date": when.isoformat(), "landowner_permission": "true", **selections}
                        key = tuple(sorted(params.items()))
                        if key not in cases:
                            cases[key] = {"params": params, "draft_keys": set()}
                        cases[key]["draft_keys"].add(draft.key)

        visited_drafts, active_ids, closed_count, no_data_count = set(), set(), 0, 0
        for case in cases.values():
            params = case["params"]
            when = date.fromisoformat(params["date"])
            applicable = [publication for publication in self.publications
                          if publication.snapshot["species_id"] == params["species"]
                          and publication.snapshot["land_type_id"] == params["land_type"]
                          and _accepts(publication.snapshot.get("scopes", {}), params)
                          and _contains(publication.snapshot["coverage"], when)]
            expected = {}
            scoped_rules = []
            for publication in applicable:
                for index, item in enumerate(publication.snapshot["rules"]):
                    if not _accepts(item.get("scopes", {}), params):
                        continue
                    scoped_rules.append(item)
                    matching_periods = [bounds for bounds in item["periods"] if _contains(bounds, when)]
                    if matching_periods and not item.get("prohibited", False):
                        expected[f"review-{publication.pk}-{index}"] = (publication, item, matching_periods)
            with self.subTest(parameters=params):
                response = self.client.get("/api/regulations/search/", params)
                self.assertEqual(response.status_code, 200, response.content)
                answer = response.json()
                actual = {item["id"]: item for item in answer["matched_seasons"]}
                self.assertEqual(set(actual), set(expected), "An open rule was omitted or leaked across date/geographic scope.")
                self.assertEqual(answer["status"], "reviewed" if expected else "closed" if applicable else "no_data")
                self.assertEqual(answer["verified"], bool(applicable))
                if applicable and not expected:
                    closed_count += 1
                    self.assertEqual(answer["eligibility"], "no_open_season")
                if not applicable:
                    no_data_count += 1
                source_map = {item["url"]: item for item in answer["sources"]}
                for public_source in answer["sources"]:
                    parsed = urlparse(public_source["url"])
                    self.assertEqual(parsed.scheme, "https")
                    self.assertTrue(parsed.hostname == "myfwc.com" or (parsed.hostname or "").endswith(".myfwc.com"))
                for identifier, (publication, item, matching_periods) in expected.items():
                    active_ids.add(identifier)
                    self.assertEqual(actual[identifier]["periods"], matching_periods)
                    self.assertEqual(actual[identifier]["publication_id"], publication.pk)
                    self.assertEqual(actual[identifier]["last_verified_at"], publication.reviewed_at.isoformat())
                    self.assertTrue(_accepts(actual[identifier]["scopes"], params))
                    for bounds in actual[identifier]["periods"]:
                        self.assertTrue(_contains(bounds, when))
                    for url in item["source_urls"]:
                        self.assertIn(url, source_map)
                        self.assertTrue(source_map[url]["last_verified_at"])
                        self.assertTrue(source_map[url]["source_checked_on"])
                if applicable:
                    for field in ["bag", "licenses", "methods"]:
                        self.assertTrue(answer[field])
                        self.assertNotIn("not recorded", answer[field].casefold())
                        self.assertNotIn("no reviewed information", answer[field].casefold())
                        self.assertNotIn("unknown", answer[field].casefold())
                    displayed = [entry[1] for entry in expected.values()] if expected else scoped_rules
                    for item in displayed:
                        messages = " ".join(answer["alerts"])
                        if "maximum_age" in item:
                            age = item["maximum_age"]
                            self.assertTrue(str(age) in messages or f"under {age + 1}" in messages,
                                            "Youth eligibility must remain visible in the answer.")
                        if "minimum_age" in item:
                            self.assertIn(str(item["minimum_age"]), messages)
                        if "YOUTH" in item["code"]:
                            self.assertTrue("15" in messages or "under 16" in messages)
                            self.assertIn("18", messages, "Youth hunting must retain the adult supervision condition.")
                visited_drafts.update(case["draft_keys"])
        self.assertEqual(visited_drafts, {draft.key for draft in self.drafts})
        self.assertGreater(closed_count, 0)
        self.assertGreater(no_data_count, 0)
        print(f"Expansion matrix: {len(self.drafts)} drafts; {periods_checked} periods; {len(cases)} public GET requests; "
              f"{len(active_ids)} distinct open rules; {closed_count} closed answers; {no_data_count} outside-coverage answers.")

    def test_existing_approved_publication_history_survives_expansion_installation(self):
        self.assertEqual(len(self.original_publications), 18)
        for original in self.original_publications:
            stored = RegulatoryPublication.objects.get(pk=original["id"])
            self.assertEqual(stored.snapshot, original["snapshot"])
            self.assertEqual(stored.revision, original["revision"])
            self.assertFalse(stored.is_current)
        self.assertEqual(RegulatoryPublication.objects.count(), len(self.drafts) + 18)
