"""Withhold a known overbroad historical answer without rewriting its history.

FWC EO23-16 section2(b/c), and the 2026-2027 Fisheating Creek brochure,
require separate east/west US27 scopes. Earlier broad publications did not
encode that distinction. They remain audit records, but cannot establish
current hunting guidance for Fisheating Creek. Replacement answers still
require the ordinary human publication workflow.
"""


def has_required_python_area_scope(snapshot, context):
    species = context.selections["species"]
    area = context.selections.get("managed_area")
    if (species.common_name.casefold() == "burmese python" and area is not None
            and area.name == "Fisheating Creek WMA"):
        return "regulatory_area" in snapshot.get("scopes", {})
    return True
