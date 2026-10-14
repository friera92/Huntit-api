from dataclasses import dataclass


@dataclass(frozen=True)
class FWCSource:
    key: str
    title: str
    url: str
    document_type: str = "Web Page"
    organization: str = (
        "Florida Fish and Wildlife "
        "Conservation Commission (FWC)"
    )


SEASON_DATES = FWCSource(
    key="season_dates",
    title=(
        "Florida Resident Game and Furbearer "
        "Hunting Season Dates and Bag Limits"
    ),
    url="https://myfwc.com/hunting/season-dates/",
)


BURMESE_PYTHON_REMOVAL = FWCSource(
    key="burmese_python_removal",
    title="Removing Pythons in Florida",
    url=(
        "https://myfwc.com/"
        "wildlifehabitats/nonnatives/python/removing/"
    ),
)

WILD_HOG = FWCSource(
    key="wild_hog",
    title="Wild Hog",
    url="https://myfwc.com/hunting/wild-hog/",
)


MIGRATORY_BIRDS = FWCSource(
    key="migratory_birds",
    title="Migratory Bird Hunting Regulations",
    url="https://myfwc.com/hunting/regulations/birds/",
)


FWC_SOURCES = {
    SEASON_DATES.key: SEASON_DATES,
    BURMESE_PYTHON_REMOVAL.key: BURMESE_PYTHON_REMOVAL,
    MIGRATORY_BIRDS.key: MIGRATORY_BIRDS,
    WILD_HOG.key: WILD_HOG,
}


def get_source(source_key):
    try:
        return FWC_SOURCES[source_key]
    except KeyError:
        available = ", ".join(FWC_SOURCES.keys())

        raise ValueError(
            f"Unknown FWC source: {source_key}. "
            f"Available sources: {available}"
        )


def get_source_keys():
    return list(FWC_SOURCES.keys())