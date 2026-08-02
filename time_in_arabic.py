#!/usr/bin/env python3
"""Compatibility wrapper for the original standalone script."""

from datetime import datetime

from src.esa3akam import (
    DEFAULT_TIMEZONE,
    day_period_to_arabic,
    format_now,
    format_time,
    hour_to_arabic,
    minute_to_arabic,
)
from src.esa3akam.cli import main


def get_d2e2a(moment: datetime) -> str:
    """Return the Arabic minute phrase used by the original API."""

    return minute_to_arabic(moment.minute)


def get_daytime(hour: int) -> str:
    """Compatibility alias for :func:`day_period_to_arabic`."""

    return day_period_to_arabic(hour)


def format_time_in_arabic(moment: datetime) -> str:
    """Compatibility alias for :func:`esa3akam.format_time`."""

    return format_time(moment)


def current_time_in_arabic(timezone_name: str = DEFAULT_TIMEZONE) -> str:
    """Compatibility alias for :func:`esa3akam.format_now`."""

    return format_now(timezone=timezone_name)


if __name__ == "__main__":
    raise SystemExit(main())
