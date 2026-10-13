import re

from regulations.services.fwc.parsers.parser import FWCMainParser
from regulations.services.fwc.parsers.bag_limit import (
    FWCBagLimitParser,
)


class FWCDeerParser(FWCMainParser):
    def parse_seasons(self, text):
        season_pattern = re.compile(
            r"("
            r"Archery season|"
            r"Crossbow season|"
            r"Muzzleloading gun season|"
            r"Youth deer hunt weekend|"
            r"General gun season"
            r")\s*:",
            re.IGNORECASE,
        )

        matches = list(season_pattern.finditer(text))

        seasons = []

        for index, match in enumerate(matches):
            start = match.end()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(text)

            season_name = match.group(1).strip()
            date_text = text[start:end].strip()

            seasons.append({
                "season_type": season_name,
                "date_text": date_text,
            })

        return seasons
    
    def parse_deer_zone(self, harvest_category, zone, season_year):
        parent_heading = f"{harvest_category} DEER"

        content = self.get_subsection_content(
            parent_heading,
            f"Zone {zone}",
        )

        if not content:
            raise ValueError(
                f"No data found for "
                f"{harvest_category} deer - Zone {zone}"
            )

        text = " ".join(content)

        seasons = self.parse_seasons(text)

        return {
            "species": "White Tailed Deer",
            "harvest_category": harvest_category.title(),
            "zone": zone.upper(),
            "season_year": season_year,
            "seasons": seasons,
        }
    
    def parse_antlerless_zone(self, zone, season_year):
        content = self.get_subsection_content(
            "ANTLERLESS DEER",
            f"Zone {zone}",
        )

        if not content:
            raise ValueError(
                f"No antlerless deer data found for Zone {zone}"
            )

        text = " ".join(content)

        seasons = self.parse_seasons(text)

        parsed_seasons = []

        for season in seasons:
            rules = self._parse_dmu_rules(
                season["date_text"]
            )

            parsed_seasons.append({
                "season_type": season["season_type"],
                "rules": rules,
            })

        return {
            "species": "White Tailed Deer",
            "harvest_category": "Antlerless",
            "zone": zone.upper(),
            "season_year": season_year,
            "seasons": parsed_seasons,
        }

    def _parse_dmu_rules(self, text):
        text = re.sub(
            r"\(\d+\)",
            "",
            text,
        ).strip()

        # If no DMU appears, the rule applies at zone level.
        if not re.search(
            r"\bDMU\b",
            text,
            re.IGNORECASE,
        ):
            return [
                {
                    "dmu": None,
                    "date_text": text,
                }
            ]

        results = []

        # Handle:
        #
        # DMU A2 and DMU A3 : Sept. 12-13
        combined_pattern = re.compile(
            r"DMU\s+([A-Z]\d+)"
            r"\s+and\s+"
            r"DMU\s+([A-Z]\d+)"
            r"\s*:\s*"
            r"(.+)",
            re.IGNORECASE,
        )

        combined_match = combined_pattern.fullmatch(
            text
        )

        if combined_match:
            first_dmu = combined_match.group(1).upper()
            second_dmu = combined_match.group(2).upper()
            date_text = combined_match.group(3).strip()

            return [
                {
                    "dmu": first_dmu,
                    "date_text": date_text,
                },
                {
                    "dmu": second_dmu,
                    "date_text": date_text,
                },
            ]

        # Handle:
        #
        # DMU C1 : Nov. 21-29
        # DMU C2 : Nov. 21-29
        # DMU C3 : Nov. 21-29
        # ...

        pattern = re.compile(
            r"DMU\s+([A-Z]\d+)\s*:\s*"
            r"(.*?)"
            r"(?=\s+DMU\s+[A-Z]\d+\s*:|$)",
            re.IGNORECASE,
        )

        for match in pattern.finditer(text):
            results.append({
                "dmu": match.group(1).upper(),
                "date_text": match.group(2).strip(),
            })

        return results

    def parse_bag_limits(self):
        content = self.get_exact_section_content(
            "Bag Limit"
        )

        if not content:
            raise ValueError(
                "No deer bag limit data found."
            )

        text = " ".join(content)

        bag_parser = FWCBagLimitParser()

        rules = bag_parser.parse_standard_limits(
            text
        )

        # Add the fields required by the common
        # HuntIt representation.
        for rule in rules:
            rule["harvest_category"] = None
            rule["dmu"] = None

        # Deer-specific rule:
        # only 2 of the annual limit may be antlerless.
        antlerless_match = re.search(
            r"only\s+(\d+)\s+can be antlerless",
            text,
            re.IGNORECASE,
        )

        if antlerless_match:
            rules.append({
                "limit_type": "ANNUAL",
                "limit": int(
                    antlerless_match.group(1)
                ),
                "is_unlimited": False,
                "harvest_category": "Antlerless",
                "dmu": None,
                "conditions": (
                    "Maximum antlerless deer within "
                    "the annual deer bag limit."
                ),
            })

        # Deer-specific DMU D2 exception.
        dmu_match = re.search(
            r"in\s+DMU\s+([A-Z]\d+),\s*"
            r"(\d+)\s+of\s+the\s+(\d+)\s+deer\s+"
            r"may\s+be\s+antlerless",
            text,
            re.IGNORECASE,
        )

        if dmu_match:
            rules.append({
                "limit_type": "ANNUAL",
                "limit": int(
                    dmu_match.group(2)
                ),
                "is_unlimited": False,
                "harvest_category": "Antlerless",
                "dmu": dmu_match.group(1).upper(),
                "conditions": (
                    "DMU-specific exception to the "
                    "general annual antlerless limit."
                ),
            })

        return {
            "species": "White Tailed Deer",
            "rules": rules,
            "note": bag_parser.extract_note(text),
        }