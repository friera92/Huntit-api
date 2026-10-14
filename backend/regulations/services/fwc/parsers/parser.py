from bs4 import BeautifulSoup


class FWCMainParser:
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

    def get_exact_section_content(self, heading_text):
        headings = self.soup.find_all(
            ["h1", "h2", "h3", "h4", "h5"]
        )

        target = None

        for heading in headings:
            text = heading.get_text(
                " ",
                strip=True,
            )

            if text.lower() == heading_text.lower():
                target = heading
                break

        if not target:
            return []

        content = []

        for element in target.find_next_siblings():
            if element.name in [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
            ]:
                break

            text = element.get_text(
                " ",
                strip=True,
            )

            if text:
                content.append(text)

        return content
    
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