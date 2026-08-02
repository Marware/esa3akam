import unittest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from esa3akam import (
    day_period_to_arabic,
    format_time,
    hour_to_arabic,
    minute_to_arabic,
)


EXPECTED_MINUTES = (
    "تمامًا",
    "دقيقة واحدة",
    "دقيقتان",
    "ثلاث دقائق",
    "أربع دقائق",
    "خمس دقائق",
    "ست دقائق",
    "سبع دقائق",
    "ثماني دقائق",
    "تسع دقائق",
    "عشر دقائق",
    "إحدى عشرة دقيقة",
    "اثنتا عشرة دقيقة",
    "ثلاث عشرة دقيقة",
    "أربع عشرة دقيقة",
    "خمس عشرة دقيقة",
    "ست عشرة دقيقة",
    "سبع عشرة دقيقة",
    "ثماني عشرة دقيقة",
    "تسع عشرة دقيقة",
    "عشرون دقيقة",
    "إحدى وعشرون دقيقة",
    "اثنتان وعشرون دقيقة",
    "ثلاث وعشرون دقيقة",
    "أربع وعشرون دقيقة",
    "خمس وعشرون دقيقة",
    "ست وعشرون دقيقة",
    "سبع وعشرون دقيقة",
    "ثمان وعشرون دقيقة",
    "تسع وعشرون دقيقة",
    "ثلاثون دقيقة",
    "إحدى وثلاثون دقيقة",
    "اثنتان وثلاثون دقيقة",
    "ثلاث وثلاثون دقيقة",
    "أربع وثلاثون دقيقة",
    "خمس وثلاثون دقيقة",
    "ست وثلاثون دقيقة",
    "سبع وثلاثون دقيقة",
    "ثمان وثلاثون دقيقة",
    "تسع وثلاثون دقيقة",
    "أربعون دقيقة",
    "إحدى وأربعون دقيقة",
    "اثنتان وأربعون دقيقة",
    "ثلاث وأربعون دقيقة",
    "أربع وأربعون دقيقة",
    "خمس وأربعون دقيقة",
    "ست وأربعون دقيقة",
    "سبع وأربعون دقيقة",
    "ثمان وأربعون دقيقة",
    "تسع وأربعون دقيقة",
    "خمسون دقيقة",
    "إحدى وخمسون دقيقة",
    "اثنتان وخمسون دقيقة",
    "ثلاث وخمسون دقيقة",
    "أربع وخمسون دقيقة",
    "خمس وخمسون دقيقة",
    "ست وخمسون دقيقة",
    "سبع وخمسون دقيقة",
    "ثمان وخمسون دقيقة",
    "تسع وخمسون دقيقة",
)


class ArabicGrammarTests(unittest.TestCase):
    def test_every_minute_has_the_approved_inflection(self):
        self.assertEqual(len(EXPECTED_MINUTES), 60)
        for minute, expected in enumerate(EXPECTED_MINUTES):
            with self.subTest(minute=minute):
                self.assertEqual(minute_to_arabic(minute), expected)

    def test_every_hour_uses_the_feminine_ordinal(self):
        expected = (
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
        for hour in range(24):
            with self.subTest(hour=hour):
                self.assertEqual(hour_to_arabic(hour), expected[hour % 12])

    def test_day_period_boundaries(self):
        expected = {
            0: "فجرًا",
            4: "فجرًا",
            5: "صباحًا",
            10: "صباحًا",
            11: "ظهرًا",
            13: "ظهرًا",
            14: "عصرًا",
            15: "عصرًا",
            16: "مساءً",
            19: "مساءً",
            20: "ليلًا",
            23: "ليلًا",
        }
        for hour, phrase in expected.items():
            with self.subTest(hour=hour):
                self.assertEqual(day_period_to_arabic(hour), phrase)


class FormatTimeTests(unittest.TestCase):
    def test_prefix_free_output(self):
        value = datetime(2026, 8, 3, 14, 6)
        self.assertEqual(format_time(value), "الثانية وست دقائق عصرًا")

    def test_day_period_can_be_omitted(self):
        value = datetime(2026, 8, 3, 14, 6)
        self.assertEqual(
            format_time(value, include_day_period=False),
            "الثانية وست دقائق",
        )

    def test_exact_hour_has_no_conjunction(self):
        value = datetime(2026, 8, 3, 0, 0)
        self.assertEqual(format_time(value), "الثانية عشرة تمامًا فجرًا")

    def test_selected_timezone_controls_clock_and_day_period(self):
        value = datetime(2026, 1, 15, 13, 0, tzinfo=timezone.utc)
        self.assertEqual(
            format_time(value, timezone="Africa/Cairo"),
            "الثالثة تمامًا عصرًا",
        )
        self.assertEqual(
            format_time(value, timezone="Asia/Tokyo"),
            "العاشرة تمامًا ليلًا",
        )

    def test_cairo_daylight_saving_offset_is_applied_before_day_period(self):
        value = datetime(2026, 8, 3, 13, 0, tzinfo=timezone.utc)
        self.assertEqual(
            format_time(value, timezone="Africa/Cairo"),
            "الرابعة تمامًا مساءً",
        )

    def test_tzinfo_instance_is_accepted(self):
        value = datetime(2026, 1, 15, 13, 0, tzinfo=timezone.utc)
        self.assertEqual(
            format_time(value, timezone=ZoneInfo("Africa/Cairo")),
            "الثالثة تمامًا عصرًا",
        )

    def test_aware_datetime_without_target_timezone_is_not_converted(self):
        value = datetime(2026, 1, 15, 13, 0, tzinfo=timezone.utc)
        self.assertEqual(format_time(value), "الواحدة تمامًا ظهرًا")

    def test_naive_datetime_is_interpreted_in_selected_timezone(self):
        value = datetime(2026, 1, 15, 13, 0)
        rendered = format_time(value, timezone="Asia/Tokyo")
        self.assertEqual(rendered, "الواحدة تمامًا ظهرًا")

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(TypeError):
            format_time("2026-08-03T14:06:00")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            format_time(datetime.now(), timezone=3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            format_time(datetime.now(), include_day_period=1)  # type: ignore[arg-type]

        invalid_values = (
            (-1, hour_to_arabic),
            (24, hour_to_arabic),
            (-1, minute_to_arabic),
            (60, minute_to_arabic),
        )
        for value, formatter in invalid_values:
            with self.subTest(value=value, formatter=formatter.__name__):
                with self.assertRaises(ValueError):
                    formatter(value)


if __name__ == "__main__":
    unittest.main()
