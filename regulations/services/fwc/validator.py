VALID_ZONES = {"A", "B", "C", "D"}

VALID_DMUS = {
    "A1", "A2", "A3",
    "B1",
    "C1", "C2", "C3", "C4", "C5", "C6",
    "D1", "D2",
}


def validate_zone(code):
    if code not in VALID_ZONES:
        raise ValueError(f"Unknown hunting zone: {code}")


def validate_dmu(code):
    if code not in VALID_DMUS:
        raise ValueError(f"Unknown deer management unit: {code}")