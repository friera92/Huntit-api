import re
from datetime import date

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "sept": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

SEASON_TYPE_MAP = {
    "archery season": "ARCHERY",
    "crossbow season": "CROSSBOW",
    "muzzleloading gun season": "MUZZLELOADING_GUN",
    "general gun season": "GENERAL_GUN",
    "youth deer hunt weekend": "YOUTH_DEER",
    "trapping season": "TRAPPING",
}


def normalize_whitespace(value):
    if not value:
        return ""

    return re.sub(r"\s+", " ", value).strip()


def normalize_zone(value):
    value = normalize_whitespace(value).upper()

    if value.startswith("ZONE "):
        return value.removeprefix("ZONE ")

    return value


def normalize_dmu(value):
    value = normalize_whitespace(value).upper()

    if value.startswith("DMU "):
        return value.removeprefix("DMU ")

    return value

def normalize_season_type(value):
    value = normalize_whitespace(value).lower()

    try:
        return SEASON_TYPE_MAP[value]
    except KeyError:
        raise ValueError(
            f"Unknown FWC season type: {value}"
        )

def normalize_periods(value, season_year):
    """
    Convert FWC date ranges into Python date objects.

    Examples:
        Aug. 1-30
        Aug. 1 – Sept. 4
        Sept. 19 – Oct. 18, Nov. 21 – Jan. 3

    season_year:
        2026-2027
    """

    value = normalize_whitespace(value)

    # Remove FWC footnote markers such as "(1)"
    value = re.sub(r"\(\d+\)", "", value).strip()

    # Normalize the different dash characters used by FWC.
    value = (
        value
        .replace("–", "-")
        .replace("—", "-")
    )

    try:
        start_year, end_year = map(
            int,
            season_year.split("-"),
        )
    except ValueError:
        raise ValueError(
            f"Invalid season year: {season_year}"
        )

    periods = []

    for period_text in value.split(","):
        period_text = period_text.strip()

        if not period_text:
            continue

        start_date, end_date = _parse_period(
            period_text,
            start_year,
            end_year,
        )

        periods.append({
            "start_date": start_date,
            "end_date": end_date,
        })

    return periods


def _parse_period(value, start_year, end_year):
    parts = re.split(r"\s*-\s*", value)

    if len(parts) != 2:
        raise ValueError(
            f"Unable to parse date range: {value}"
        )

    start_text, end_text = parts

    start_month, start_day = _parse_month_day(
        start_text
    )

    # "Aug. 1-30"
    # The end date doesn't repeat the month.
    if re.fullmatch(r"\d{1,2}", end_text.strip()):
        end_month = start_month
        end_day = int(end_text.strip())

    else:
        end_month, end_day = _parse_month_day(
            end_text
        )

    start_date = date(
        start_year,
        start_month,
        start_day,
    )

    # Example:
    #
    # Nov. 21 - Jan. 3
    #
    # January belongs to the second year of
    # the hunting season.
    if end_month < start_month:
        period_end_year = end_year
    else:
        period_end_year = start_year

    end_date = date(
        period_end_year,
        end_month,
        end_day,
    )

    return start_date, end_date


def _parse_month_day(value):
    match = re.fullmatch(
        r"([A-Za-z]+)\.?\s*(\d{1,2})",
        value.strip(),
    )

    if not match:
        raise ValueError(
            f"Unable to parse date: {value}"
        )

    month_name = match.group(1).lower()
    day = int(match.group(2))

    try:
        month = MONTHS[month_name]
    except KeyError:
        raise ValueError(
            f"Unknown month: {month_name}"
        )

    return month, day