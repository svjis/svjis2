import re
from django.conf import settings


def is_bot(user_agent: str) -> bool:
    spoofing = getattr(settings, 'SVJIS_SPOOFING_USER_AGENTS', [])
    bots = [r'curl', r'bot', r'crawler', r'spider', r'scrapy', r'agency']

    if not re.search(r'^Mozilla/5\.0 \(', user_agent):
        return True

    if user_agent in spoofing:
        return True

    for b in bots:
        if re.search(b, user_agent, re.IGNORECASE):
            return True

    return False


def get_browser(user_agent: str) -> dict:
    browsers = {
        'yabrowser': r'YaBrowser\/(\d+\.?\d*)',
        'edge': r'Edg\/(\d+\.?\d*)|EdgiOS\/(\d+\.?\d*)',
        'opera': r'Opera\/(\d+\.?\d*)|OPR\/(\d+\.?\d*)|OPT\/(\d+\.?\d*)',
        'firefox': r'Firefox\/(\d+\.?\d*)',
        'safari': r'Version\/(\d+\.?\d*)',
        'samsung': r'SamsungBrowser\/(\d+\.?\d*)',
        'crios': r'CriOS\/(\d+\.?\d*)',
        'ie': r'MSIE (\d+\.?\d*)|Trident.*rv:(\d+\.?\d*)',
        'chrome': r'Chrome\/(\d+\.?\d*)',
    }

    if not is_bot(user_agent):
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


def get_os(user_agent: str) -> dict:
    ua = user_agent.lower()
    patterns = {
        r'windows nt': 'Windows:Desktop',
        r'iphone os': 'iOS:Mobile',
        r'mac os x': 'macOS:Desktop',
        r'android': 'Android:Mobile',
        r'linux': 'Linux:Desktop',
        r'ubuntu': 'Ubuntu:Desktop',
    }

    if not is_bot(user_agent):
        for pattern, result in patterns.items():
            match = re.search(pattern, ua)
            if match:
                r = str(result).split(':')
                return {'os': r[0], 'platform': r[1]}

    return {'os': 'Unknown', 'platform': 'Unknown'}
