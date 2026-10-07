from regulations.services.fwc.parsers.parser import (
    FWCMainParser,
)


class FWCBurmesePythonParser(FWCMainParser):

    PRIVATE_LAND_PREFIX = "Hunting on Private Land:"

    MANAGED_LAND_PREFIX = (
        "Hunting on Commission-managed lands:"
    )

    MANAGED_LANDS_HEADING = (
        "Online Brochures for the 32 "
        "Commission-managed Lands"
    )

    def _get_paragraph_starting_with(
        self,
        prefix,
    ):
        for paragraph in self.soup.find_all("p"):
            text = paragraph.get_text(
                " ",
                strip=True,
            )

            if text.lower().startswith(
                prefix.lower()
            ):
                return text

        return ""

    def get_private_land_rules(self):
        return self._get_paragraph_starting_with(
            self.PRIVATE_LAND_PREFIX
        )

    def get_managed_land_rules(self):
        return self._get_paragraph_starting_with(
            self.MANAGED_LAND_PREFIX
        )

    def get_managed_lands(self):
        heading = None

        for candidate in self.soup.find_all(
            ["h2", "h3", "h4"]
        ):
            text = candidate.get_text(
                " ",
                strip=True,
            )

            if (
                text.lower()
                == self.MANAGED_LANDS_HEADING.lower()
            ):
                heading = candidate
                break

        if not heading:
            return []

        lands = []

        for element in heading.find_all_next():
            if (
                element.name
                in ["h1", "h2", "h3", "h4"]
                and element is not heading
            ):
                break

            if element.name == "li":
                name = element.get_text(
                    " ",
                    strip=True,
                )

                if name:
                    lands.append(
                        {
                            "name": name,
                            "area_type": self._infer_area_type(name)
                        }
                    )

        return lands

    def _infer_area_type(self, name):
        upper_name = name.upper()

        # Check the more specific cases first.
        if "SMALL GAME AREA" in upper_name:
            return "SGA"

        if "NATIONAL WILDLIFE REFUGE" in upper_name:
            return "NWR"

        if "PSGHA" in upper_name:
            return "PSGHA"

        if "WEA" in upper_name:
            return "WEA"

        if "WMA" in upper_name:
            return "WMA"

        return "OTHER"

    def parse_private_land_rules(self, season_year):
        text = self.get_private_land_rules()

        if not text:
            raise ValueError(
                "No Burmese Python private land "
                "regulations found."
            )

        return {
            "species": "Burmese Python",
            "land_type": "Private Land",
            "season_type": "Year-Round",
            "season_year": season_year,
            "harvest_category": None,
            "bag_limit": {
                "limit_type": "GENERAL",
                "limit": None,
                "is_unlimited": True,
                "conditions": "",
            },
            "note": {
                "title": (
                    "Private Land Burmese Python "
                    "Regulations"
                ),
                "text": text,
            },
        }

    def parse_managed_land_rules(self, season_year):
        text = self.get_managed_land_rules()

        if not text:
            raise ValueError(
                "No Burmese Python managed land "
                "regulations found."
            )

        areas = self.get_managed_lands()

        if not areas:
            raise ValueError(
                "No Burmese Python managed areas found."
            )

        return {
            "species": "Burmese Python",
            "land_type": "Commission-Managed Land",
            "season_type": "Year-Round",
            "season_year": season_year,
            "harvest_category": None,
            "managed_areas": areas,
            "bag_limit": {
                "limit_type": "GENERAL",
                "limit": None,
                "is_unlimited": True,
                "conditions": (
                    "Area-specific rules also apply."
                ),
            },
            "note": {
                "title": (
                    "Commission-Managed Land "
                    "Burmese Python Regulations"
                ),
                "text": text,
            },
        }