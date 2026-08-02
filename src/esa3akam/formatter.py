"""Arabic clock-time formatting."""

from __future__ import annotations

from datetime import datetime, tzinfo
from typing import Optional, Union
from zoneinfo import ZoneInfo


DEFAULT_TIMEZONE = "Africa/Cairo"
TimezoneLike = Union[str, tzinfo]

# The hour is an ordinal adjective describing the feminine noun "الساعة".
# Midnight and noon both map to index zero after modulo 12.
_HOUR_NAMES = (
    "الثانية عشرة",
    "الواحدة",
    "الثانية",
    "الثالثة",
    "الرابعة",
    "الخامسة",
    "السادسة",
    "السابعة",
    "الثامنة",
    "التاسعة",
    "العاشرة",
    "الحادية عشرة",
)

# Forms used with the feminine counted noun "دقيقة". For 3–10, the numeral
# takes the opposite grammatical gender and the counted noun is plural.
_MINUTE_UNITS = {
    3: "ثلاث",
    4: "أربع",
    5: "خمس",
    6: "ست",
    7: "سبع",
    8: "ثماني",
    9: "تسع",
    10: "عشر",
}
_COMPOUND_MINUTE_UNITS = {
    1: "إحدى",
    2: "اثنتان",
    3: "ثلاث",
    4: "أربع",
    5: "خمس",
    6: "ست",
    7: "سبع",
    8: "ثمان",
    9: "تسع",
}
_TENS = {
    20: "عشرون",
    30: "ثلاثون",
    40: "أربعون",
    50: "خمسون",
}


def _validate_clock_part(value: int, name: str, upper_bound: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if not 0 <= value < upper_bound:
        raise ValueError(f"{name} must be between 0 and {upper_bound - 1}")


def _coerce_timezone(value: TimezoneLike) -> tzinfo:
    if isinstance(value, str):
        return ZoneInfo(value)
    if isinstance(value, tzinfo):
        return value
    raise TypeError("timezone must be an IANA timezone name or tzinfo instance")


def _normalize_datetime(value: datetime, timezone: Optional[TimezoneLike]) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("value must be a datetime instance")
    if timezone is None:
        return value

    target_timezone = _coerce_timezone(timezone)
    if value.utcoffset() is None:
        # With no source offset there is nothing to convert. Interpret the
        # supplied fields as wall-clock time in the selected timezone.
        return value.replace(tzinfo=target_timezone)
    return value.astimezone(target_timezone)


def hour_to_arabic(hour: int) -> str:
    """Return the Arabic ordinal name for an hour in 24-hour notation."""

    _validate_clock_part(hour, "hour", 24)
    return _HOUR_NAMES[hour % 12]


def minute_to_arabic(minute: int) -> str:
    """Return a grammatically inflected Arabic phrase for ``minute``."""

    _validate_clock_part(minute, "minute", 60)

    if minute == 0:
        return "تمامًا"
    if minute == 1:
        return "دقيقة واحدة"
    if minute == 2:
        return "دقيقتان"
    if minute <= 10:
        return f"{_MINUTE_UNITS[minute]} دقائق"
    if minute == 11:
        return "إحدى عشرة دقيقة"
    if minute == 12:
        return "اثنتا عشرة دقيقة"
    if minute < 20:
        return f"{_MINUTE_UNITS[minute - 10]} عشرة دقيقة"

    ones = minute % 10
    tens = _TENS[minute - ones]
    if ones == 0:
        return f"{tens} دقيقة"
    return f"{_COMPOUND_MINUTE_UNITS[ones]} و{tens} دقيقة"


def day_period_to_arabic(hour: int) -> str:
    """Return the conventional Arabic day-period label for ``hour``."""

    _validate_clock_part(hour, "hour", 24)

    if hour < 5:
        return "فجرًا"
    if hour < 11:
        return "صباحًا"
    if hour < 14:
        return "ظهرًا"
    if hour < 16:
        return "عصرًا"
    if hour < 20:
        return "مساءً"
    return "ليلًا"


def format_time(
    value: datetime,
    *,
    timezone: Optional[TimezoneLike] = None,
    include_day_period: bool = True,
) -> str:
    """Render ``value`` as Arabic clock text.

    If ``value`` is timezone-aware and ``timezone`` is supplied, the instant is
    converted to the selected timezone before both its clock time and day-period
    label are rendered. A naive value is treated as wall-clock time in the
    selected timezone, because it has no source offset from which to convert.
    """

    if not isinstance(include_day_period, bool):
        raise TypeError("include_day_period must be a boolean")

    effective_value = _normalize_datetime(value, timezone)
    hour = hour_to_arabic(effective_value.hour)
    minute = minute_to_arabic(effective_value.minute)
    conjunction = " " if effective_value.minute == 0 else " و"
    rendered = f"{hour}{conjunction}{minute}"

    if include_day_period:
        rendered = f"{rendered} {day_period_to_arabic(effective_value.hour)}"
    return rendered


def format_now(
    *,
    timezone: TimezoneLike = DEFAULT_TIMEZONE,
    include_day_period: bool = True,
) -> str:
    """Render the current time in ``timezone`` as Arabic clock text."""

    selected_timezone = _coerce_timezone(timezone)
    return format_time(
        datetime.now(selected_timezone),
        include_day_period=include_day_period,
    )
