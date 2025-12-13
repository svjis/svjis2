from pathlib import Path
import tomllib  # Python 3.11+, use tomli for older versions


def get_version():
    """Get SVJIS version"""
    try:
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)
        return pyproject_data["project"]["version"]
    except Exception:
        return "unknown"


__version__ = get_version()
