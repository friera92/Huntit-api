import re
from datetime import date

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
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
    "fall turkey season": "FALL_TURKEY",
    "youth turkey hunt": "YOUTH_TURKEY",
    "spring turkey season": "SPRING_TURKEY",
    "year-round": "YEAR_ROUND",
    "year round": "YEAR_ROUND",
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

def normalize_periods(value, season_year, initial_year=None):
    """
    Convert FWC date ranges into Python date objects.

    Examples:
        Aug. 1-30
        Aug. 1 – Sept. 4
        Sept. 19 – Oct. 18, Nov. 21 – Jan. 3
        Dec. 5-11, Feb. 22 – 28

    season_year:
        2026-2027
    """

    value = normalize_whitespace(value)

    # Remove FWC footnotes such as "(1)"
    value = re.sub(r"\(\d+\)", "", value).strip()

    # Normalize dash characters.
    value = (
        value
        .replace("–", "-")
        .replace("—", "-")
    )

    try:
        first_year, second_year = map(
            int,
            season_year.split("-"),
        )
    except ValueError:
        raise ValueError(
            f"Invalid season year: {season_year}"
        )

    if initial_year is None:
        current_year = first_year
    else:
        if initial_year not in {first_year, second_year}:
            raise ValueError(
                f"{initial_year} is outside "
                f"season {season_year}"
            )
    
        current_year = initial_year

    periods = []

    previous_start_month = None

    for period_text in value.split(","):
        period_text = period_text.strip()

        if not period_text:
            continue

        start_month, start_day, end_month, end_day = (
            _parse_period_parts(period_text)
        )

        # Example:
        #
        # Dec. 5-11, Feb. 22-28
        #
        # The month goes from 12 -> 2,
        # so the second period belongs to the next year.
        if (
            previous_start_month is not None
            and start_month < previous_start_month
        ):
            current_year += 1

            if current_year > second_year:
                raise ValueError(
                    f"Date range exceeds season "
                    f"{season_year}"
                )

        start_date = date(
            current_year,
            start_month,
            start_day,
        )

        # A single period may itself cross the year:
        #
        # Dec. 26 - Jan. 3
        if end_month < start_month:
            end_date_year = current_year + 1
        else:
            end_date_year = current_year

        if end_date_year > second_year:
            raise ValueError(
                f"Date range exceeds season "
                f"{season_year}"
            )
        
        end_date = date(
            end_date_year,
            end_month,
            end_day,
        )

        periods.append({
            "start_date": start_date,
            "end_date": end_date,
        })

        previous_start_month = start_month

    return periods


def _parse_period_parts(value):
    parts = re.split(
        r"\s*-\s*",
        value,
    )

    if len(parts) != 2:
        raise ValueError(
            f"Unable to parse date range: {value}"
        )

    start_text, end_text = parts

    start_month, start_day = _parse_month_day(
        start_text
    )

    # Example:
    #
    # Aug. 1-30
    #
    # The end date does not repeat the month.
    if re.fullmatch(
        r"\d{1,2}",
        end_text.strip(),
    ):
        end_month = start_month
        end_day = int(end_text.strip())

    else:
        end_month, end_day = _parse_month_day(
            end_text
        )

    return (
        start_month,
        start_day,
        end_month,
        end_day,
    )


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

    print(f"Month: {month_name}, Day: {day}")

    try:
        month = MONTHS[month_name]
    except KeyError:
        raise ValueError(
            f"Unknown month: {month_name}"
        )

    return month, day