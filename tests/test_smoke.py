import sys
from pathlib import Path

import pytest
import tomli
from packaging.specifiers import SpecifierSet
from packaging.version import Version

pytestmark = pytest.mark.smoke

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def supported_python_specifier() -> SpecifierSet:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as file:
        pyproject = tomli.load(file)

    return SpecifierSet(pyproject["project"]["requires-python"])


def test_current_python_is_supported() -> None:
    current_version = Version(
        f"{sys.version_info.major}.{sys.version_info.minor}."
        f"{sys.version_info.micro}"
    )

    assert current_version in supported_python_specifier(), (
        f"Python {current_version} não atende à restrição definida no "
        "pyproject.toml."
    )
