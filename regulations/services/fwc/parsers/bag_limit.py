import re


class FWCBagLimitParser:

    STANDARD_PATTERNS = {
        "DAILY": (
            r"Daily bag limit\s*:\s*(\d+)"
        ),
        "POSSESSION": (
            r"Possession limit\s*:\s*(\d+)"
        ),
        "ANNUAL": (
            r"Annual bag limit\s*:\s*(\d+)"
        ),
    }

    def parse_standard_limits(self, text):
        rules = []

        for limit_type, pattern in (
            self.STANDARD_PATTERNS.items()
        ):
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                rules.append({
                    "limit_type": limit_type,
                    "limit": int(match.group(1)),
                    "is_unlimited": False,
                    "conditions": "",
                })

        return rules

    def extract_note(self, text):
        match = re.search(
            r"NOTE:\s*(.+)$",
            text,
            re.IGNORECASE,
        )

        if not match:
            return ""

        return match.group(1).strip()

    def has_no_limit(self, text):
        return bool(
            re.search(
                r"\bno\s+limit\b",
                text,
                re.IGNORECASE,
            )
        )