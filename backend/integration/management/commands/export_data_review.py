"""Export the exact working additions for a human to compare with FWC."""
import hashlib
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from integration.data_expansion import EDITION
from integration.engine import ComplianceEngine
from integration.models import RegulationDraft
from regulations.models import DeerManagementUnit, HuntingZone, LandType, ManagedArea, RegulatoryArea, Species


class Command(BaseCommand):
    help = "Export data-expansion review JSON/Markdown. This does not approve or publish anything."

    def add_arguments(self, parser):
        parser.add_argument("--output-dir", required=True)

    def handle(self, *args, **options):
        folder = Path(options["output_dir"]).resolve()
        folder.mkdir(parents=True, exist_ok=True)
        entries = []
        names = {
            "zone": dict(HuntingZone.objects.values_list("pk", "code")),
            "dmu": dict(DeerManagementUnit.objects.values_list("pk", "code")),
            "managed_area": dict(ManagedArea.objects.values_list("pk", "name")),
            "regulatory_area": dict(RegulatoryArea.objects.values_list("pk", "name")),
        }
        rows = list(RegulationDraft.objects.select_related("species", "land_type").order_by("key"))
        for row in rows:
            if row.payload.get("data_expansion_edition") != EDITION and not (
                    row.key.endswith("-expanded") or row.key.startswith("turkey-private-")):
                continue
            row.full_clean()
            entries.append({"key": row.key, "title": row.title, "species": row.species.common_name,
                            "land_type": row.land_type.name,
                            "change": "proposed revision of existing approved draft" if row.publications.exists() else "new draft",
                            "payload": row.payload})
        document = {"edition": EDITION, "source_checked_on": "2026-10-12", "human_approval": None,
                    "publication_status": "DRAFT — HUMAN SOURCE REVIEW REQUIRED",
                    "catalog": {"species": list(Species.objects.values("id", "common_name")),
                                "land_types": list(LandType.objects.values("id", "name")), **names},
                    "drafts": entries}
        content = (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        digest = hashlib.sha256(content).hexdigest()
        (folder / "DATA_EXPANSION_REVIEW.json").write_bytes(content)
        lines = ["# HuntIt data expansion — source review pack", "",
                 "**Status: source-checked working data; human approval and publication remain pending.**", "",
                 f"Edition: `{EDITION}`. Source check: 2026-10-12. Exact JSON SHA-256: `{digest}`.", "",
                 f"This pack contains **{len(entries)} draft scopes/revisions**. The two public-land selectors repeat the same area rules; they are not additional areas.", "",
                 "Compare the dates, methods, limits, licenses, area exceptions and profile below with the linked FWC sources. Publication requires explicit human source-review approval. Existing regulatory content and approval dates are preserved.", "",
                 "After checking, an authorized reviewer can publish each draft in Django Admin, using the source acknowledgement and review notes. Saving alone does not publish. Repeating setup preserves edited drafts and withdrawn publications.", "",
                 "## Coverage index", "", "| Draft | Species / land | Change |", "|---|---|---|"]
        lines += [f"| `{entry['key']}` | {entry['species']} / {entry['land_type']} | {entry['change']} |" for entry in entries]
        for entry in entries:
            payload = entry["payload"]
            scopes = []
            for field, values in payload.get("scopes", {}).items():
                values = values if isinstance(values, list) else [values]
                scopes.append(field + ": " + ", ".join(str(names[field].get(value, value)) for value in values))
            lines += ["", "## " + entry["title"], "", f"Key: `{entry['key']}`. {entry['change']}.", "",
                      "Scope: " + ("; ".join(scopes) or "Private-land statewide exception"), "",
                      "Review coverage: " + payload["coverage"]["start_date"] + " through " + payload["coverage"]["end_date"] + ".", ""]
            for source in payload["sources"]:
                lines += [f"- [{source['title']}]({source['url']}) — checked {source['checked_on']}. {source['evidence']}"]
            for rule in payload["rules"]:
                lines += ["", "### " + rule["name"] + " / " + rule["category"], "",
                          "Dates: " + "; ".join(ComplianceEngine.period_label(period) for period in rule["periods"]), "",
                          "Bag: " + rule["bag"], "", "Licenses: " + rule["licenses"], "", "Methods: " + rule["methods"], ""]
                if rule.get("prohibited"):
                    lines += ["**Explicit prohibition. Search must remain closed throughout these dates.**", ""]
                lines += ["- " + alert for alert in rule.get("alerts", [])]
            lines += ["", "Conditions for the whole scope:", ""] + ["- " + alert for alert in payload.get("alerts", [])]
            if payload.get("species_information"):
                lines += ["", "Proposed completion of blank species fields:", ""]
                lines += [f"- {key}: {value}" for key, value in payload["species_information"].items() if key != "source_urls"]
        (folder / "DATA_EXPANSION_REVIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.stdout.write(f"Exported {len(entries)} review entries. SHA-256 {digest}. Nothing published.")
