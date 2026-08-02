"""Command-line interface for :mod:`esa3akam`."""

from __future__ import annotations

import argparse
from typing import Optional, Sequence
from zoneinfo import ZoneInfoNotFoundError

from .formatter import DEFAULT_TIMEZONE, format_now


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="esa3akam",
        description="Render the current time as Arabic text.",
    )
    parser.add_argument(
        "--timezone",
        default=DEFAULT_TIMEZONE,
        help=f"IANA timezone name (default: {DEFAULT_TIMEZONE})",
    )
    parser.add_argument(
        "--no-day-period",
        action="store_true",
        help="omit the day-period label",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        rendered = format_now(
            timezone=args.timezone,
            include_day_period=not args.no_day_period,
        )
    except ZoneInfoNotFoundError:
        parser.error(f"unknown timezone: {args.timezone}")

    print(rendered)
    return 0
