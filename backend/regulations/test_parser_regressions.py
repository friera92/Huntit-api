"""Offline parser regressions; test passages are not verified hunting guidance."""

import json
from html import escape
from pathlib import Path

from django.test import SimpleTestCase

from .services.fwc.parsers.python import FWCBurmesePythonParser
from .services.fwc.parsers.wild_hog import FWCWildHogParser


class PythonManagedHeadingTests(SimpleTestCase):
    def test_original_and_changed_numeric_counts_select_only_the_exact_section(self):
        for count in [32, 33, 100]:
            with self.subTest(count=count):
                html = f"""
                    <h2>Unrelated managed lands</h2>
                    <ul><li>Unrelated WMA</li></ul>
                    <h2>Online Brochures for the {count} Commission-managed Lands</h2>
                    <ul><li>Synthetic WMA</li><li>Synthetic WEA</li></ul>
                    <h2>Other resources</h2>
                    <ul><li>Outside WMA</li></ul>
                """
                areas = FWCBurmesePythonParser(html).get_managed_lands()
                self.assertEqual(areas, [
                    {"name": "Synthetic WMA", "area_type": "WMA"},
                    {"name": "Synthetic WEA", "area_type": "WEA"},
                ])

    def test_unrelated_or_partial_headings_are_not_accepted(self):
        for heading in [
            "Online Brochures for the 33 Unrelated Lands",
            "Online Brochures for the 33 Commission-managed Lands Archive",
            "Historical Online Brochures for the 33 Commission-managed Lands",
            "Online Brochures for the many Commission-managed Lands",
        ]:
            with self.subTest(heading=heading):
                html = f"<h2>{heading}</h2><ul><li>Unrelated WMA</li></ul>"
                self.assertEqual(FWCBurmesePythonParser(html).get_managed_lands(), [])


class WildHogBagLimitTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture = Path(__file__).resolve().parents[1] / "integration" / "fixtures" / "demo_regulations.json"
        records = json.loads(fixture.read_text(encoding="utf-8"))
        cls.known_note = next(
            record["fields"]["text"]
            for record in records
            if record["model"] == "regulations.regulationnote"
            and record["fields"]["title"] == "Private Land Wild Hog Regulations"
        )

    def parse_note(self, text):
        html = f"<h1>Wild Hog</h1><h2>Hunting</h2><p>{escape(text)}</p>"
        return FWCWildHogParser(html).parse_private_land_rules("2026-2027")

    def test_known_local_snapshot_has_consistent_unlimited_output(self):
        result = self.parse_note(self.known_note)
        self.assertTrue(result["bag_limit"]["is_unlimited"])
        self.assertIsNone(result["bag_limit"]["limit"])
        self.assertEqual(result["bag_limit"]["conditions"], "No size or bag limit.")

    def test_changed_limit_passage_requires_review_instead_of_unlimited_output(self):
        changed = self.known_note.replace("no size or bag limit", "a daily bag limit of 2")
        self.assertNotEqual(changed, self.known_note)
        with self.assertRaisesMessage(ValueError, "review the source"):
            self.parse_note(changed)

    def test_missing_limit_passage_also_requires_review(self):
        with self.assertRaisesMessage(ValueError, "review the source"):
            self.parse_note("Wild hogs may be hunted year-round with landowner permission.")
