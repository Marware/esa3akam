# esa3akam

`esa3akam` renders clock times as grammatically inflected Modern Standard
Arabic text.

```text
الثانية وست دقائق عصرًا
```

It supports timezone conversion, optional day-period labels, and both library
and command-line use. Python 3.9 or newer is required, and the test matrix
currently covers CPython 3.9 through the Python 3.15 prerelease.

## Installation

```bash
python -m pip install esa3akam
```

## Library usage

Format a wall-clock datetime:

```python
from datetime import datetime

from esa3akam import format_time

value = datetime(2026, 8, 3, 14, 6)
print(format_time(value))
# الثانية وست دقائق عصرًا
```

Hide the day-period label when it is not needed:

```python
format_time(value, include_day_period=False)
# الثانية وست دقائق
```

Convert a timezone-aware datetime before formatting it:

```python
from datetime import datetime, timezone

value = datetime(2026, 1, 15, 13, 0, tzinfo=timezone.utc)

format_time(value, timezone="Africa/Cairo")
# الثالثة تمامًا عصرًا

format_time(value, timezone="Asia/Tokyo")
# العاشرة تمامًا ليلًا
```

The selected timezone is applied before both the clock value and its day-period
label are calculated. A naive `datetime` has no source offset, so supplying a
timezone interprets its existing fields as wall-clock time in that timezone.

Render the current time in Cairo or another timezone:

```python
from esa3akam import format_now

format_now()  # Africa/Cairo by default
format_now(timezone="Asia/Riyadh", include_day_period=False)
```

The lower-level `hour_to_arabic`, `minute_to_arabic`, and
`day_period_to_arabic` functions are also public for applications that need to
assemble their own output.

## Command line

```bash
esa3akam
esa3akam --timezone Asia/Riyadh
esa3akam --no-day-period
```

The original script remains available when running from the source repository:

```bash
python3 time_in_arabic.py
```

## Language rules

The package emits Modern Standard Arabic without full vocalization. Hour names
use feminine ordinals because `الساعة` is feminine. Minute numerals are
inflected for the feminine noun `دقيقة`, including the special forms for 1–2,
3–10, 11–19, and compound numerals through 59.

Day periods use these boundaries:

- `00:00–04:59`: `فجرًا`
- `05:00–10:59`: `صباحًا`
- `11:00–13:59`: `ظهرًا`
- `14:00–15:59`: `عصرًا`
- `16:00–19:59`: `مساءً`
- `20:00–23:59`: `ليلًا`

## Development

Run the tests directly from a source checkout:

```bash
PYTHONPATH=src python3 -m unittest discover -v
```

The project is licensed under Apache-2.0. It was originally made for fun for
the Facebook page
[يا عمو الساعة كام؟](https://www.facebook.com/ya3amoelsa3akam/).
