import re

from regulations.services.fwc.parsers.parser import (
    FWCMainParser,
)

from regulations.services.fwc.parsers.bag_limit import (
    FWCBagLimitParser,
)


class FWCTurkeyParser(FWCMainParser):

    FALL_SEASONS = [
        "Archery season",
        "Crossbow season",
        "Muzzleloading gun season",
        "Fall turkey season",
    ]

    SPRING_SEASONS = [
        "Youth turkey hunt",
        "Spring turkey season",
    ]

    SPRING_AREAS = {
        "NORTH_SR70": {
            "name": "North of State Road 70",
        },
        "SOUTH_SR70": {
            "name": "South of State Road 70",
        },
    }

    def _parse_seasons(self, text, season_names):
        pattern = re.compile(
            r"("
            + "|".join(
                re.escape(name)
                for name in season_names
            )
            + r")\s*:\s*",
            re.IGNORECASE,
        )

        matches = list(pattern.finditer(text))

        seasons = []

        for index, match in enumerate(matches):
            start = match.end()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(text)

            date_text = text[start:end].strip()

            seasons.append({
                "season_type": match.group(1),
                "date_text": date_text,
            })

        return seasons

    def parse_fall_zone(self, zone, season_year):
        content = self.get_subsection_content(
            "TURKEY",
            f"Zone {zone}",
        )

        if not content:
            raise ValueError(
                f"No Fall Turkey data found "
                f"for Zone {zone}."
            )

        text = " ".join(content)

        first_year = int(
            season_year.split("-")[0]
        )

        return {
            "species": "Wild Turkey",
            "harvest_category": (
                "Gobbler and Bearded Turkey"
            ),
            "season_group": "FALL",
            "zone": zone.upper(),
            "regulatory_area": None,
            "season_year": season_year,
            "initial_year": first_year,
            "seasons": self._parse_seasons(
                text,
                self.FALL_SEASONS,
            ),
        }

    def parse_spring_area(self, area_code, season_year):
        try:
            area = self.SPRING_AREAS[
                area_code
            ]
        except KeyError:
            raise ValueError(
                f"Unknown Turkey regulatory area: "
                f"{area_code}"
            )

        heading = area["name"]

        content = self.get_exact_section_content(
            heading
        )

        if not content:
            raise ValueError(
                f"No Spring Turkey data found "
                f"for {heading}."
            )

        text = " ".join(content)

        second_year = int(
            season_year.split("-")[1]
        )

        return {
            "species": "Wild Turkey",
            "harvest_category": (
                "Gobbler and Bearded Turkey"
            ),
            "season_group": "SPRING",
            "zone": None,

            "regulatory_area": {
                "code": area_code,
                "name": heading,
            },

            "season_year": season_year,
            "initial_year": second_year,
            "seasons": self._parse_seasons(
                text,
                self.SPRING_SEASONS,
            ),
        }

    def parse_bag_limits(self, season_group):
        season_group = season_group.upper()

        if season_group == "FALL":
            heading = "Fall Seasons"

        elif season_group == "SPRING":
            heading = "Spring seasons (2)"

        else:
            raise ValueError(
                f"Unknown Turkey season group: "
                f"{season_group}"
            )

        content = self.get_exact_section_content(
            heading
        )

        if not content:
            raise ValueError(
                f"No Turkey bag limits found "
                f"for {season_group}."
            )

        text = " ".join(content)

        bag_parser = FWCBagLimitParser()

        rules = []

        daily_match = re.search(
            r"Daily bag limit\s*:\s*(\d+)",
            text,
            re.IGNORECASE,
        )

        if daily_match:
            rules.append({
                "limit_type": "DAILY",
                "limit": int(
                    daily_match.group(1)
                ),
                "is_unlimited": False,
                "conditions": "",
            })

        combined_match = re.search(
            r"Season and possession limit\s*:\s*"
            r"(\d+)\s+for\s+(.+)$",
            text,
            re.IGNORECASE,
        )

        if combined_match:
            limit = int(
                combined_match.group(1)
            )

            conditions = (
                combined_match
                .group(2)
                .strip()
            )

            rules.append({
                "limit_type": "SEASON",
                "limit": limit,
                "is_unlimited": False,
                "conditions": conditions,
            })

            rules.append({
                "limit_type": "POSSESSION",
                "limit": limit,
                "is_unlimited": False,
                "conditions": conditions,
            })

        for rule in rules:
            rule["harvest_category"] = (
                "Gobbler and Bearded Turkey"
            )

            rule["season_group"] = (
                season_group
            )

        return {
            "species": "Wild Turkey",
            "season_group": season_group,
            "rules": rules,
        }