from pathlib import Path
import tomllib  # Python 3.11+, use tomli for older versions


def get_value_from_pyproject_toml(table: str, key: str) -> str:
    """Get value from pyptoject.toml"""
    try:
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)

        data = pyproject_data
        for part in table.split("."):
            data = data[part]
        return data[key]
    except Exception:
        return ""


__version__: str = get_value_from_pyproject_toml("project", "version")
__homepage_url__: str = get_value_from_pyproject_toml("project.urls", "Homepage")
__repository_url__: str = get_value_from_pyproject_toml("project.urls", "Repository")
__issues_url__: str = get_value_from_pyproject_toml("project.urls", "Issues")
__translations_url__: str = get_value_from_pyproject_toml("project.urls", "Translations")
