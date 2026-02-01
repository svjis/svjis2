from django.test import TestCase
from ..user_agent import get_browser, get_os


class UserAgentTests(TestCase):
    cases = [
        # Firefox on Linux
        {
            "agent": [
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",  # noqa
            ],
            "browser": "Firefox",
            "os": {'os': 'Linux', 'platform': 'Desktop'},
        },
        # Firefox on Windows
        {
            "agent": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",  # noqa
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",  # noqa
            ],
            "browser": "Firefox",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        # Firefox on Android
        {
            "agent": [
                "Mozilla/5.0 (Android 15; Mobile; rv:144.0) Gecko/144.0 Firefox/144.0",  # noqa
            ],
            "browser": "Firefox",
            "os": {'os': 'Android', 'platform': 'Mobile'},
        },
        # Safari on iOS
        {
            "agent": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0.1 Mobile/15E148 Safari/604.1",  # noqa
                "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",  # noqa
                "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",  # noqa
            ],
            "browser": "Safari",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        # Safari on Macintosh
        {
            "agent": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15",  # noqa
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",  # noqa
            ],
            "browser": "Safari",
            "os": {'os': 'macOS', 'platform': 'Desktop'},
        },
        # Chrome on Android
        {
            "agent": [
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",  # noqa
            ],
            "browser": "Chrome",
            "os": {'os': 'Android', 'platform': 'Mobile'},
        },
        # Chrome on Windows
        {
            "agent": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",  # noqa
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",  # noqa
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36",  # noqa
            ],
            "browser": "Chrome",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        # Chrome on Linux
        {
            "agent": [
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",  # noqa
            ],
            "browser": "Chrome",
            "os": {'os': 'Linux', 'platform': 'Desktop'},
        },
        # Chrome on Macintosh
        {
            "agent": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  # noqa
            ],
            "browser": "Chrome",
            "os": {'os': 'macOS', 'platform': 'Desktop'},
        },
        # Edge on iOS
        {
            "agent": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.65 Version/17.0 Mobile/15E148 Safari/604.1",  # noqa
            ],
            "browser": "Edge",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        # Edge on iOS
        {
            "agent": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",  # noqa
            ],
            "browser": "Edge",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        # Samsung Browser on Android
        {
            "agent": [
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/29.0 Chrome/136.0.0.0 Mobile Safari/537.36",  # noqa
            ],
            "browser": "Samsung",
            "os": {'os': 'Android', 'platform': 'Mobile'},
        },
        # CriOS on iOS
        {
            "agent": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 26_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/142.0.7444.128 Mobile/15E148 Safari/604.1",  # noqa
            ],
            "browser": "Crios",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        # Opera on iOS
        {
            "agent": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.2.3",  # noqa
            ],
            "browser": "Opera",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        # YaBrowser on Windows
        {
            "agent": [
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/22.7.0 Yowser/2.5 Safari/537.36",  # noqa
            ],
            "browser": "Yabrowser",
            "os": {'os': 'Windows', 'platform': 'Desktop'},
        },
        # SznProhlizec on Android
        {
            "agent": [
                "Mozilla/5.0 (Linux; Android 15; SM-S721B Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.171 Mobile Safari/537.36 SznProhlizec/12.6.0a",  # noqa
            ],
            "browser": "SznProhlizec",
            "os": {'os': 'Android', 'platform': 'Mobile'},
        },
        # SznProhlizec on Macintosh
        {
            "agent": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.7.2 Safari/605.1.15 SznProhlizec/15.1.0i",  # noqa
                "Mozilla/5.0 (iPhone; CPU OS 26_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Mobile/15e148 Safari/605.1.15 SznProhlizec/15.1.0i",  # noqa
            ],
            "browser": "SznProhlizec",
            "os": {'os': 'macOS', 'platform': 'Desktop'},
        },
        # DuckDuckGo on iOS
        {
            "agent": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_12 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1 Ddg/16.7",  # noqa
            ],
            "browser": "DuckDuckGo",
            "os": {'os': 'iOS', 'platform': 'Mobile'},
        },
        # HuaweiBrowser on HarmonyOS
        {
            "agent": [
                "Mozilla/5.0 (Linux; Android 12; HarmonyOS; CLS-AL30; HMSCore 6.15.4.332) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 HuaweiBrowser/16.0.12.301 Mobile Safari/537.36",  # noqa
            ],
            "browser": "HuaweiBrowser",
            "os": {'os': 'HarmonyOS', 'platform': 'Mobile'},
        },
        # Bots
        {
            "agent": [
                "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/116",  # noqa
                "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot",  # noqa
                "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",  # noqa
                "Mozilla/5.0 (compatible; Barkrowler/0.9; +https://babbar.tech/crawler)",  # noqa
                "Sidetrade indexer bot",
                "Sidetrade indexer Bot",
                "Mozilla/5.0 X11; Ubuntu; Linux x86_64; rv:126.0 Gecko/20100101 Firefox/126.0",  # noqa
                "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"",  # noqa
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Agency/98.8.8175.80",  # noqa
            ],
            "browser": "Unknown",
            "os": {'os': 'Unknown', 'platform': 'Unknown'},
        },
    ]

    def test_browser(self):
        for case in self.cases:
            for a in case.get("agent"):
                result = get_browser(a)
                self.assertEqual(result.get("browser", ""), case.get("browser", ""), f"User-agent: {a}")

    def test_os(self):
        for case in self.cases:
            for a in case.get("agent"):
                result = get_os(a)
                self.assertEqual(result, case.get("os", ""), f"User-agent: {a}")
