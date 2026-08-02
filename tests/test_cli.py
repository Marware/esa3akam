import contextlib
import io
import unittest
from unittest.mock import patch

from esa3akam.cli import main


class CommandLineTests(unittest.TestCase):
    @patch("esa3akam.cli.format_now", return_value="الثانية وست دقائق عصرًا")
    def test_cli_forwards_timezone_and_prints_result(self, format_now):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result = main(["--timezone", "Asia/Riyadh"])

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue(), "الثانية وست دقائق عصرًا\n")
        format_now.assert_called_once_with(
            timezone="Asia/Riyadh",
            include_day_period=True,
        )

    @patch("esa3akam.cli.format_now", return_value="الثانية وست دقائق")
    def test_cli_can_omit_day_period(self, format_now):
        with contextlib.redirect_stdout(io.StringIO()):
            result = main(["--no-day-period"])

        self.assertEqual(result, 0)
        format_now.assert_called_once_with(
            timezone="Africa/Cairo",
            include_day_period=False,
        )

    def test_unknown_timezone_is_reported_as_cli_error(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                main(["--timezone", "Not/A_Timezone"])

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("unknown timezone: Not/A_Timezone", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
