import re

from regulations.services.fwc.parsers.parser import (
    FWCMainParser,
)


class FWCWildHogParser(FWCMainParser):

    def _get_content_heading(self, heading_text):
        page_title = self.soup.find(
            "h1",
            string=lambda text: (
                text
                and text.strip().lower()
                == "wild hog"
            ),
        )

        if not page_title:
            raise ValueError(
                "Wild Hog page title was not found."
            )

        heading = page_title.find_next(
            lambda tag: (
                tag.name
                in ["h2", "h3", "h4", "h5", "h6"]
                and tag.get_text(
                    " ",
                    strip=True,
                ).lower()
                == heading_text.lower()
            )
        )

        return heading

    def _extract_heading_content(self, heading):
        if not heading:
            return []

        heading_level = int(
            heading.name[1]
        )

        content = []

        for element in heading.find_all_next():
            if element is heading:
                continue

            if (
                element.name
                in ["h1", "h2", "h3", "h4", "h5", "h6"]
            ):
                level = int(
                    element.name[1]
                )

                if level <= heading_level:
                    break

            if element.name in ["p", "li"]:
                text = element.get_text(
                    " ",
                    strip=True,
                )

                if text:
                    content.append(text)

        return content

    def get_private_land_rules(self):
        heading = self._get_content_heading(
            "Hunting"
        )

        return self._extract_heading_content(
            heading
        )

    def get_public_land_rules(self):
        return self.get_exact_section_content(
            "Wild Hog Hunting on FWC Public "
            "Hunting Areas "
            "(including Wildlife Management Areas)"
        )

    def parse_private_land_rules(self,season_year):
        content = self.get_private_land_rules()

        if not content:
            raise ValueError(
                "No Wild Hog private land "
                "regulations found."
            )

        text = " ".join(content)

        if not re.search(
            r"\byear-round\b",
            text,
            re.IGNORECASE,
        ):
            raise ValueError(
                "Expected year-round Wild Hog "
                "regulation was not found."
            )

        is_unlimited = bool(
            re.search(
                r"no\s+size\s+or\s+bag\s+limit",
                text,
                re.IGNORECASE,
            )
        )

        either_sex = bool(
            re.search(
                r"either\s+sex\s+may\s+be\s+harvested",
                text,
                re.IGNORECASE,
            )
        )

        legal_methods = (
            self._extract_legal_methods(text)
        )

        return {
            "species": "Wild Hog",
            "land_type": "Private Land",
            "harvest_category": (
                "Either Sex"
                if either_sex
                else None
            ),
            "season_type": "Year-Round",
            "season_year": season_year,
            "legal_methods": legal_methods,
            "bag_limit": {
                "limit_type": "GENERAL",
                "limit": None,
                "is_unlimited": is_unlimited,
                "conditions": (
                    "No size or bag limit."
                ),
            },
            "note": {
                "title": (
                    "Private Land Wild Hog Regulations"
                ),
                "text": text,
            },
        }

    def parse_public_land_note(self, season_year):
        content = self.get_public_land_rules()

        if not content:
            raise ValueError(
                "No Wild Hog WMA regulations found."
            )

        text = " ".join(content)

        return {
            "species": "Wild Hog",
            "season_year": season_year,
            "title": (
                "WMA-Specific Wild Hog Regulations"
            ),
            "text": text,
        }

    def _extract_legal_methods(self, text):
        methods = []

        method_patterns = {
            "Rifle": r"\brifle\b",
            "Shotgun": r"\bshotgun\b",
            "Crossbow": r"\bcrossbow\b",
            "Bow": r"\bbow\b",
            "Pistol": r"\bpistol\b",
            "Air Gun": r"\bair\s+gun\b",
            "Dogs": r"\bdogs?\b",
            "Live Trap": r"\blive\s+traps?\b",
        }

        for name, pattern in method_patterns.items():
            if re.search(
                pattern,
                text,
                re.IGNORECASE,
            ):
                methods.append(name)

        return methods