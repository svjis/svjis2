from django.test import TestCase
from ..user_agent import get_browser, get_os


class UserAgentTests(TestCase):
    cases = [
        {
            "agent": "Mozilla/5.0 X11; Ubuntu; Linux x86_64; rv:126.0 Gecko/20100101 Firefox/126.0",  # noqa
            "browser": "Firefox",
            "os": {'os': 'Linux', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",  # noqa
            "browser": "Safari",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",  # noqa
            "browser": "Firefox",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Android', 'platform': 'Mobile'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0.1 Mobile/15E148 Safari/604.1",  # noqa
            "browser": "Safari",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",  # noqa
            "browser": "Firefox",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",  # noqa
            "browser": "Safari",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        {
            "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",  # noqa
            "browser": "Safari",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        {
            "agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'Linux', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",  # noqa
            "browser": "Edge",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        {
            "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  # noqa
            "browser": "Chrome",
            "os": {'os': 'macOS', 'platform': 'Desktop'},
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
