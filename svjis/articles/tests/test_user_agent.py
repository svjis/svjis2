from django.test import TestCase
from ..user_agent import get_browser, get_os


class UserAgentTests(TestCase):
    cases = [
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": "Windows 10",
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
            "browser": "Firefox",
            "os": "Windows 10",
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": "Windows 10",
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",  # noqa
            "browser": "Edge",
            "os": "Windows 10",
        },
    ]

    def test_browser(self):
        for case in self.cases:
            result = get_browser(case.get("agent"))
            self.assertEqual(result.get("browser", ""), case.get("browser", ""))

    def test_os(self):
        for case in self.cases:
            result = get_os(case.get("agent"))
            self.assertEqual(result, case.get("os", ""))
