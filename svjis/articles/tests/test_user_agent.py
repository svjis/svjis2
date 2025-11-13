from django.test import TestCase
from ..user_agent import get_browser, get_os


class UserAgentTests(TestCase):
    cases = [
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
            "browser": "Firefox",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",  # noqa
            "browser": "Edge",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Android', 'platform': 'Mobile'},
        },
        {
            "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",  # noqa
            "browser": "Safari",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
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
