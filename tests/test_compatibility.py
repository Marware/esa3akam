import unittest
from datetime import datetime

import time_in_arabic


class CompatibilityTests(unittest.TestCase):
    def test_original_helpers_delegate_to_the_package(self):
        value = datetime(2026, 8, 3, 14, 42)
        self.assertEqual(time_in_arabic.get_d2e2a(value), "اثنتان وأربعون دقيقة")
        self.assertEqual(time_in_arabic.get_daytime(14), "عصرًا")
        self.assertEqual(
            time_in_arabic.format_time_in_arabic(value),
            "الثانية واثنتان وأربعون دقيقة عصرًا",
        )


if __name__ == "__main__":
    unittest.main()
