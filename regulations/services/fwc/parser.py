import re

from bs4 import BeautifulSoup


class FWCSeasonParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")

    def get_text(self):
        return self.soup.get_text(
            separator="\n",
            strip=True,
        )

    def get_headings(self):
        headings = []

        for heading in self.soup.find_all(
            ["h1", "h2", "h3", "h4", "h5"]
        ):
            text = heading.get_text(" ", strip=True)

            if text:
                headings.append({
                    "level": heading.name,
                    "text": text,
                })

        return headings
    
    def get_section_content(self, heading_text):
        heading = self.soup.find(
            lambda tag: (
                tag.name in ["h1", "h2", "h3", "h4", "h5"]
                and heading_text.lower()
                in tag.get_text(" ", strip=True).lower()
            )
        )

        if not heading:
            return []

        content = []

        for element in heading.find_next_siblings():
            if element.name in ["h1", "h2", "h3", "h4", "h5"]:
                break

            text = element.get_text(
                " ",
                strip=True,
            )

            if text:
                content.append(text)

        return content

    def get_subsection_content(self, parent_heading_text, subsection_heading_text):
        headings = self.soup.find_all(
            ["h1", "h2", "h3", "h4", "h5"]
        )

        inside_parent = False

        for heading in headings:
            text = heading.get_text(
                " ",
                strip=True,
            )

            if parent_heading_text.lower() in text.lower():
                inside_parent = True
                continue

            if inside_parent:
                if subsection_heading_text.lower() == text.lower():
                    content = []

                    for element in heading.find_next_siblings():
                        if element.name in [
                            "h1",
                            "h2",
                            "h3",
                            "h4",
                            "h5",
                        ]:
                            break

                        value = element.get_text(
                            " ",
                            strip=True,
                        )

                        if value:
                            content.append(value)

                    return content

        return []

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
    
    def parse_antlerless_zone(self, zone, season_year,):
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
            dmu_periods = self._parse_dmu_periods(
                season["date_text"]
            )

            parsed_seasons.append({
                "season_type": season["season_type"],
                "dmu_periods": dmu_periods,
            })

        return {
            "species": "White Tailed Deer",
            "harvest_category": "Antlerless",
            "zone": zone.upper(),
            "season_year": season_year,
            "seasons": parsed_seasons,
        }

    def _parse_dmu_periods(self, text):
        # Remove FWC footnote markers.
        text = re.sub(r"\(\d+\)", "", text).strip()

        results = []

        # Handle:
        #
        # DMU A2 and DMU A3 : Sept. 12-13
        #
        combined_pattern = re.compile(
            r"DMU\s+([A-Z]\d+)"
            r"\s+and\s+"
            r"DMU\s+([A-Z]\d+)"
            r"\s*:\s*"
            r"(.+)",
            re.IGNORECASE,
        )

        combined_match = combined_pattern.fullmatch(text)

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
        # DMU A2 : Aug. 1-9 DMU A3 : Aug. 1-16

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