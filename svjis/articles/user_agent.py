import re


def get_browser(user_agent: str) -> dict:
    browsers = {
        'edge': r'Edg\/(\d+\.?\d*)',
        'opera': r'Opera\/(\d+\.?\d*)|OPR\/(\d+\.?\d*)',
        'firefox': r'Firefox\/(\d+\.?\d*)',
        'safari': r'Version\/(\d+\.?\d*)',
        'ie': r'MSIE (\d+\.?\d*)|Trident.*rv:(\d+\.?\d*)',
        'chrome': r'Chrome\/(\d+\.?\d*)',
    }

    for browser, pattern in browsers.items():
        match = re.search(pattern, user_agent)
        if match:
            version = (
                match.group(1) or match.group(2)
                if match.lastindex is not None and match.lastindex > 1
                else match.group(1)
            )
            return {'browser': browser.title(), 'version': version, 'user_agent': user_agent}

    return {'browser': 'Unknown', 'version': 'Unknown', 'user_agent': user_agent}


def get_os(user_agent: str) -> str:
    ua = user_agent.lower()
    patterns = {
        r'windows nt 10\.0': 'Windows 10',
        r'windows nt 6\.1': 'Windows 7',
        r'mac os x 10[._](\d+)': lambda m: f'macOS 10.{m.group(1)}',
        r'iphone os (\d+)[._](\d+)': lambda m: f'iOS {m.group(1)}.{m.group(2)}',
        r'android (\d+\.?\d*)': lambda m: f'Android {m.group(1)}',
        r'linux': 'Linux',
        r'ubuntu': 'Ubuntu',
    }

    for pattern, result in patterns.items():
        match = re.search(pattern, ua)
        if match:
            if callable(result):
                return result(match)
            return str(result)

    return 'Unknown OS'
